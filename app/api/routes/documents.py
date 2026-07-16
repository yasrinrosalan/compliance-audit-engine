import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.models import Document, DocumentChunk
from app.services.schemas import DocumentResponse, SearchQuery, SearchResult
from app.services.tasks import process_document_task
from app.services.ai_client import get_embedding
from app.services.llm_client import generate_answer

router = APIRouter()

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """Ingests a document, saves it, and triggers the background worker."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    db_document = Document(filename=file.filename, status="pending")
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    file_path = os.path.join(UPLOAD_DIR, f"{db_document.id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_document_task.delay(db_document.id, file_path)

    return db_document

@router.post("/search", response_model=List[SearchResult])
async def semantic_search(
    query: SearchQuery, 
    db: Session = Depends(get_db)
):
    """Performs a vector similarity search."""
    try:
        query_vector = get_embedding(query.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Client Error: {str(e)}")

    results = (
        db.query(
            DocumentChunk,
            Document.filename,
            DocumentChunk.embedding.cosine_distance(query_vector).label("distance")
        )
        .join(Document, DocumentChunk.document_id == Document.id)
        .order_by("distance")
        .limit(query.top_k)
        .all()
    )

    formatted_results = []
    for chunk, filename, distance in results:
        formatted_results.append(SearchResult(
            document_id=chunk.document_id,
            filename=filename,
            content=chunk.content,
            similarity_score=round((1 - distance) * 100, 2) 
        ))

    return formatted_results

@router.post("/ask")
async def ask_question(query: SearchQuery, db: Session = Depends(get_db)):
    """Retrieves relevant chunks and generates a synthesized LLM answer."""
    try:
        query_vector = get_embedding(query.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    results = (
        db.query(DocumentChunk, Document.filename, DocumentChunk.embedding.cosine_distance(query_vector).label("distance"))
        .join(Document, DocumentChunk.document_id == Document.id)
        .order_by("distance")
        .limit(3)
        .all()
    )

    if not results:
        return {"answer": "No relevant documents found.", "sources": []}

    context = "\n\n".join([result[0].content for result in results])
    
    answer = generate_answer(context, query.query)
    
    return {
        "answer": answer, 
        "sources": list(set([result[1] for result in results]))
    }