from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine, Base
from app.services import models
from app.api.routes import documents

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Compliance Audit Engine",
    description="Enterprise Document Compliance & Semantic Audit Engine API",
    version="1.0.0"
)

app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "compliance-audit-api"}