"""
UserSelection model for the Integrated RAG Chatbot.
"""
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class UserSelectionBase(BaseModel):
    book_id: UUID
    selected_text: str
    start_pos: Optional[int] = None  # Start position in the text if available
    end_pos: Optional[int] = None    # End position in the text if available
    chapter: Optional[str] = None
    section: Optional[str] = None
    page_number: Optional[int] = None


class UserSelectionCreate(UserSelectionBase):
    pass


class UserSelection(UserSelectionBase):
    selection_id: UUID


# Note: This model may be used for tracking user selections in a more complex implementation.
# For the current requirements, the selected text is passed directly in the query request.