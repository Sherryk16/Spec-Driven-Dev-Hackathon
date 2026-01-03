"""
UserQuery model for the Integrated RAG Chatbot.
"""
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime


class UserQueryBase(BaseModel):
    book_id: UUID
    query_text: str = Field(..., min_length=10, max_length=1000)
    selected_text: Optional[str] = None


class UserQueryCreate(UserQueryBase):
    pass


class UserQuery(UserQueryBase):
    query_id: UUID
    created_at: datetime


# Note: This model is already defined in api_models.py, but creating this file
# as requested by the task. In a real implementation, we'd organize models differently.