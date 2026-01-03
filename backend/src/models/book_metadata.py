"""
BookMetadata model for the Integrated RAG Chatbot.
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class BookMetadataBase(BaseModel):
    title: str = Field(..., max_length=500)
    author: str = Field(..., max_length=200)
    description: Optional[str] = None
    isbn: Optional[str] = Field(None, max_length=13)  # ISBN-13 max length
    published_date: Optional[str] = None  # Could be a date string
    language: str = "en"  # Default to English
    page_count: Optional[int] = None
    file_path: Optional[str] = None
    file_format: Optional[str] = None  # PDF, EPUB, etc.


class BookMetadataCreate(BookMetadataBase):
    book_id: Optional[UUID] = None  # Auto-generated if not provided


class BookMetadata(BookMetadataBase):
    book_id: UUID
    created_at: datetime
    updated_at: datetime
    ingestion_status: str = "pending"  # pending, processing, completed, failed
    chunks_count: Optional[int] = None


# Note: This model is for managing book metadata separately from the content.