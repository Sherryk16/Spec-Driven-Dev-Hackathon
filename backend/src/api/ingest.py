"""
Ingestion API endpoints for the Integrated RAG Chatbot.
"""
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import Optional
import time
import tempfile
import os
from uuid import UUID, uuid4
from src.models.api_models import IngestionResponse
from src.services.ingestion_service import ingestion_service
from src.utils.logger import rag_logger, LogCategory
from src.config.settings import settings


router = APIRouter()


@router.post("/", response_model=IngestionResponse)
async def ingest_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    book_id: Optional[str] = Form(None)
):
    """
    Ingest a book file (PDF, EPUB, or Text) and process it for RAG queries.
    """
    start_time = time.time()
    
    # Validate file type
    file_ext = os.path.splitext(file.filename)[1].lower()
    allowed_extensions = ['.pdf', '.epub', '.txt', '.text']
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
        )
    
    # Check file size
    # Move the file pointer to the end to get the size
    file.file.seek(0, 2)  # Seek to end of file
    file_size = file.file.tell()
    file.file.seek(0)  # Reset file pointer to beginning
    
    # Check if file exceeds maximum size (50MB as per requirements)
    max_size_bytes = settings.MAX_BOOK_SIZE_CHARS  # Using char limit as size proxy
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is {max_size_bytes} bytes."
        )
    
    book_uuid = uuid4() if not book_id else UUID(book_id)
    
    try:
        rag_logger.log_ingestion(
            "Starting book ingestion process",
            {
                "filename": file.filename,
                "title": title,
                "author": author,
                "book_id": str(book_uuid),
                "file_size": file_size,
                "file_type": file_ext
            }
        )
        
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process the book file
            success, chunks_processed = await ingestion_service.ingest_book(
                file_path=temp_file_path,
                book_id=book_uuid,
                title=title,
                author=author
            )
            
            if not success:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to process the book file"
                )
            
            processing_time = time.time() - start_time
            
            response = IngestionResponse(
                status="success",
                book_id=book_uuid,
                title=title,
                chunks_processed=chunks_processed,
                processing_time=f"{processing_time:.2f}s"
            )
            
            rag_logger.log_ingestion(
                "Successfully completed book ingestion",
                {
                    "book_id": str(book_uuid),
                    "title": title,
                    "chunks_processed": chunks_processed,
                    "processing_time": processing_time
                }
            )
            
            return response
            
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
    except HTTPException:
        raise
    except Exception as e:
        rag_logger.log_error(
            LogCategory.INGESTION,
            f"Error during book ingestion: {str(e)}",
            {
                "filename": file.filename,
                "title": title,
                "author": author,
                "book_id": str(book_uuid) if 'book_uuid' in locals() else 'unknown',
                "exception": str(e)
            },
            e
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error during ingestion"
        )