import os
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.services.models import Document, DocumentChunk
from app.services.pdf_parser import extract_and_chunk_pdf
from app.services.ai_client import get_embedding  

@celery_app.task(bind=True)
def process_document_task(self, document_id: int, file_path: str):
    db = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return {"error": "Document not found"}

        document.status = "processing"
        db.commit()

        print(f"Extracting and chunking {document.filename}...")
        chunks = extract_and_chunk_pdf(file_path)

        for chunk_text in chunks:
            
            vector = get_embedding(chunk_text) 
            chunk_record = DocumentChunk(
                document_id=document.id,
                content=chunk_text,
                embedding=vector 
            )
            db.add(chunk_record)
        
        document.status = "completed"
        db.commit()
        
        print(f"Successfully created {len(chunks)} chunks for document {document_id}")
        return {"message": f"Processed {len(chunks)} chunks."}
        
    except Exception as e:
        if document:
            document.status = "failed"
            db.commit()
        print(f"Task failed: {e}")
    finally:
        db.close()