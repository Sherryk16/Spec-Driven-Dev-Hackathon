"""
Chat API endpoints for the Integrated RAG Chatbot.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional
import time
from uuid import UUID, uuid4
from src.models.api_models import (
    QueryRequest, 
    QuerySelectedTextRequest, 
    QueryResponse, 
    IngestionResponse,
    ChatRequest
)
from src.services.ingestion_service import ingestion_service
from src.services.retrieval_service import retrieval_service
from src.services.generation_service import generation_service
from src.utils.logger import rag_logger, LogCategory
from src.config.settings import settings


router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_book_content(request: QueryRequest):
    """
    Submit a question about the book content and receive an answer with citations.
    """
    start_time = time.time()
    
    try:
        rag_logger.log_api(
            "Received query request",
            {
                "query": request.query,
                "book_id": str(request.book_id),
                "session_id": str(request.session_id) if request.session_id else None
            }
        )
        
        # Retrieve relevant chunks from the specified book
        retrieved_chunks = await retrieval_service.retrieve_relevant_chunks(
            query=request.query,
            book_id=request.book_id
        )
        
        # Generate an answer based on the retrieved chunks
        generated_response = await generation_service.generate_answer(
            query=request.query,
            retrieved_chunks=retrieved_chunks,
            is_selected_text_query=False
        )
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Check if response time exceeds the maximum allowed
        if response_time > settings.MAX_RESPONSE_TIME:
            rag_logger.log_api(
                "Response time exceeded maximum allowed",
                {
                    "query": request.query,
                    "response_time": response_time,
                    "max_allowed": settings.MAX_RESPONSE_TIME
                }
            )
        
        response = QueryResponse(
            response_id=uuid4(),  # Generate a new UUID for this response
            answer=generated_response.response_text,
            citations=generated_response.citations,
            query_time=response_time
        )
        
        rag_logger.log_api(
            "Successfully processed query",
            {
                "query": request.query,
                "response_length": len(generated_response.response_text),
                "citations_count": len(generated_response.citations),
                "response_time": response_time
            }
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        rag_logger.log_error(
            LogCategory.API,
            f"Error processing query: {str(e)}",
            {
                "query": request.query,
                "book_id": str(request.book_id),
                "exception": str(e)
            },
            e
        )
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your query"
        )



@router.post("/query-selected-text", response_model=QueryResponse)
async def query_selected_text_content(request: QuerySelectedTextRequest):
    """
    Submit a question about user-selected text and receive an answer limited to that text.
    """
    start_time = time.time()
    
    try:
        rag_logger.log_api(
            "Received selected text query request",
            {
                "query": request.query,
                "book_id": str(request.book_id),
                "selected_text_length": len(request.selected_text),
                "session_id": str(request.session_id) if request.session_id else None
            }
        )
        
        # Retrieve relevant content from the selected text only
        retrieved_chunks = await retrieval_service.retrieve_from_selected_text(
            query=request.query,
            selected_text=request.selected_text
        )
        
        # Generate an answer based on the retrieved chunks from selected text
        generated_response = await generation_service.generate_answer(
            query=request.query,
            retrieved_chunks=retrieved_chunks,
            is_selected_text_query=True
        )
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Check if response time exceeds the maximum allowed
        if response_time > settings.MAX_RESPONSE_TIME:
            rag_logger.log_api(
                "Response time exceeded maximum allowed for selected text query",
                {
                    "query": request.query,
                    "response_time": response_time,
                    "max_allowed": settings.MAX_RESPONSE_TIME
                }
            )
        
        response = QueryResponse(
            response_id=uuid4(),  # Generate a new UUID for this response
            answer=generated_response.response_text,
            citations=generated_response.citations,
            query_time=response_time
        )
        
        rag_logger.log_api(
            "Successfully processed selected text query",
            {
                "query": request.query,
                "response_length": len(generated_response.response_text),
                "citations_count": len(generated_response.citations),
                "response_time": response_time
            }
        )
        
        return response

    except HTTPException:
        raise
    except Exception as e:
        rag_logger.log_error(
            LogCategory.API,
            f"Error processing selected text query: {str(e)}",
            {
                "query": request.query,
                "book_id": str(request.book_id),
                "selected_text_length": len(request.selected_text),
                "exception": str(e)
            },
            e
        )
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your query"
        )


@router.post("/", response_model=QueryResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint for the chatbot.
    """
    start_time = time.time()

    try:
        rag_logger.log_api(
            "Received chat request",
            {
                "query": request.query,
                "session_id": str(request.session_id) if request.session_id else None
            }
        )

        # For a RAG chatbot, we need to retrieve relevant content from ingested books
        # Since we don't have a specific book_id in this endpoint, we'll retrieve from all available books
        retrieved_chunks = await retrieval_service.retrieve_relevant_chunks(
            query=request.query,
            book_id=None  # This will search across all books
        )

        # If no chunks were retrieved from all books, inform the user
        if not retrieved_chunks or len(retrieved_chunks) == 0:
            # Inform the user that they need to ingest a book first
            response_text = (
                "The chatbot is ready to answer questions from ingested books. "
                "No book content is currently available in the system. "
                "Please ingest a book first using the /ingest endpoint with a PDF, EPUB, or text file."
            )

            response = QueryResponse(
                response_id=uuid4(),
                answer=response_text,
                citations=[],
                query_time=time.time() - start_time
            )
        else:
            generated_response = await generation_service.generate_answer(
                query=request.query,
                retrieved_chunks=retrieved_chunks,
                is_selected_text_query=False
            )

            response = QueryResponse(
                response_id=uuid4(),
                answer=generated_response.response_text,
                citations=generated_response.citations,
                query_time=time.time() - start_time
            )

        rag_logger.log_api(
            "Successfully processed chat request",
            {
                "query": request.query,
                "response_length": len(response.answer),
                "citations_count": len(response.citations),
                "response_time": response.query_time
            }
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        rag_logger.log_error(
            LogCategory.API,
            f"Error processing chat request: {str(e)}",
            {
                "query": request.query,
                "exception": str(e)
            },
            e
        )
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your chat query"
        )
