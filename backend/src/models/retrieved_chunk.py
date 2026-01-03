"""
RetrievedChunk model for the Integrated RAG Chatbot.
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class RetrievedChunk(BaseModel):
    retrieval_id: UUID
    query_id: UUID
    chunk_id: UUID
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    content: str
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None
    created_at: datetime


# Note: This model is already defined in api_models.py, but creating this file
# as requested by the task. In a real implementation, we'd organize models differently.