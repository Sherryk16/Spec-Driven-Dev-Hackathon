"""
GeneratedResponse model for the Integrated RAG Chatbot.
"""
from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime
from .api_models import Citation  # Importing from the main API models file


class GeneratedResponseBase(BaseModel):
    query_id: UUID
    response_text: str
    citations: List[Citation]
    is_fallback_response: bool = False


class GeneratedResponse(GeneratedResponseBase):
    response_id: UUID
    created_at: datetime


# Note: This model is already defined in api_models.py, but creating this file
# as requested by the task. In a real implementation, we'd organize models differently.