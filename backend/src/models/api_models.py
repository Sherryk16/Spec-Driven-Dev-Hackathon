"""
Pydantic models for the Integrated RAG Chatbot API requests/responses.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
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


class TextChunkBase(BaseModel):
    book_id: UUID
    content: str = Field(..., min_length=1, max_length=10000)
    chunk_index: int
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None


class TextChunk(TextChunkBase):
    chunk_id: UUID
    created_at: datetime


class UserQueryBase(BaseModel):
    book_id: UUID
    query_text: str = Field(..., min_length=10, max_length=1000)
    selected_text: Optional[str] = None


class UserQuery(UserQueryBase):
    query_id: UUID
    created_at: datetime


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


class Citation(BaseModel):
    chunk_id: UUID
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None


class GeneratedResponseBase(BaseModel):
    query_id: UUID
    response_text: str
    citations: List[Citation]
    is_fallback_response: bool = False


class GeneratedResponse(GeneratedResponseBase):
    response_id: UUID
    created_at: datetime


class QueryRequest(BaseModel):
    book_id: UUID
    query: str
    session_id: Optional[UUID] = None


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[UUID] = None


class QuerySelectedTextRequest(BaseModel):
    book_id: UUID
    query: str
    selected_text: str
    session_id: Optional[UUID] = None


class QueryResponse(BaseModel):
    response_id: UUID
    answer: str
    citations: List[Citation]
    query_time: float


class IngestionResponse(BaseModel):
    status: str
    book_id: UUID
    title: str
    chunks_processed: int
    processing_time: str


class HealthStatus(BaseModel):
    status: str
    timestamp: datetime
    dependencies: Dict[str, str]