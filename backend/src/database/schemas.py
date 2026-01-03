"""
SQLAlchemy models for the Integrated RAG Chatbot database interactions.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class BookContentDB(Base):
    __tablename__ = "book_content"

    book_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    author = Column(String(200), nullable=False)
    content = Column(Text)  # Can be None for metadata-only entries
    file_path = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class TextChunkDB(Base):
    __tablename__ = "text_chunks"

    chunk_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("book_content.book_id"), nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chapter = Column(String(200))
    section = Column(String(200))
    page_number = Column(Integer)
    embedding_vector = Column(Text)  # Store as JSON string or use a vector extension if available
    created_at = Column(DateTime, server_default=func.now())


class UserQueryDB(Base):
    __tablename__ = "user_queries"

    query_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("book_content.book_id"), nullable=False)
    query_text = Column(Text, nullable=False)
    selected_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class RetrievedChunkDB(Base):
    __tablename__ = "retrieved_chunks"

    retrieval_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("user_queries.query_id"), nullable=False)
    chunk_id = Column(UUID(as_uuid=True), ForeignKey("text_chunks.chunk_id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class GeneratedResponseDB(Base):
    __tablename__ = "generated_responses"

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_id = Column(UUID(as_uuid=True), ForeignKey("user_queries.query_id"), nullable=False)
    response_text = Column(Text, nullable=False)
    citations = Column(Text)  # Store as JSON string
    is_fallback_response = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class UserSessionDB(Base):
    __tablename__ = "user_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))  # Optional, for tracking
    book_id = Column(UUID(as_uuid=True), ForeignKey("book_content.book_id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    last_accessed = Column(DateTime, server_default=func.now(), onupdate=func.now())