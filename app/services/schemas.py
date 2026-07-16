from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from typing import List

class DocumentResponse(BaseModel):
    id: int
    filename: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True 
    
class SearchQuery(BaseModel):
    query: str
    top_k: int = 5 

class SearchResult(BaseModel):
    document_id: int
    filename: str
    content: str
    similarity_score: float