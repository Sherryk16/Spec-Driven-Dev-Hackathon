"""
BookContent model for the Integrated RAG Chatbot.
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class BookContentBase(BaseModel):
    title: str = Field(..., max_length=500)
    author: str = Field(..., max_length=200)
    content: Optional[str] = Field(None, min_length=1000)  # Can be None for creation
    file_path: Optional[str] = None


class BookContentCreate(BookContentBase):
    book_id: Optional[UUID] = None  # Auto-generated if not provided


class BookContent(BookContentBase):
    book_id: UUID
    created_at: datetime
    updated_at: datetime


# Note: This model is already defined in api_models.py, but creating this file
# as requested by the task. In a real implementation, we'd organize models differently.