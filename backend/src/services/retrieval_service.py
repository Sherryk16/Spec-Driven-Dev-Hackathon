"""
Retrieval service for the Integrated RAG Chatbot.
Handles vector search in Qdrant and proper citation capabilities.
"""
from typing import List, Optional
from uuid import UUID
# Try to import real services, fall back to mock if they fail
try:
    from src.vector_store.qdrant_service import qdrant_service
    from src.services.cohere_service import cohere_client
except Exception:
    from src.vector_store.mock_qdrant_service import qdrant_service
    from src.services.mock_cohere_service import cohere_client
from src.models.api_models import RetrievedChunk, Citation
from src.utils.logger import rag_logger, LogCategory
from src.config.settings import settings


class RetrievalService:
    def __init__(self):
        pass
    
    async def retrieve_relevant_chunks(
        self,
        query: str,
        book_id: Optional[UUID] = None,
        top_k: Optional[int] = None
    ) -> List[RetrievedChunk]:
        """
        Retrieve the most relevant text chunks for a given query from a specific book or across all books.

        Args:
            query: The user's query
            book_id: The ID of the book to search within. If None, search across all books.
            top_k: Number of top results to return (defaults to settings.TOP_K)

        Returns:
            List of RetrievedChunk objects with content and citations
        """
        if top_k is None:
            top_k = settings.TOP_K

        try:
            if book_id:
                rag_logger.log_retrieval(
                    f"Starting retrieval for query in book {book_id}",
                    {"query": query, "book_id": str(book_id), "top_k": top_k}
                )
            else:
                rag_logger.log_retrieval(
                    "Starting retrieval for query across all books",
                    {"query": query, "top_k": top_k}
                )

            # Generate embedding for the query
            query_embeddings = cohere_client.generate_embeddings([query])
            if not query_embeddings or len(query_embeddings) == 0:
                rag_logger.log_error(
                    LogCategory.RETRIEVAL,
                    "Failed to generate embedding for query",
                    {"query": query, "book_id": str(book_id) if book_id else "all books"}
                )
                return []

            query_embedding = query_embeddings[0]

            # Search in Qdrant for relevant chunks
            search_results = qdrant_service.search(
                query_embedding=query_embedding,
                book_id=book_id,
                top_k=top_k
            )

            # For debugging, let's see what's in the mock storage
            if hasattr(qdrant_service, 'points'):
                print(f"DEBUG: Total points in mock Qdrant: {len(qdrant_service.points)}")
                if book_id:
                    book_points = [p for p in qdrant_service.points.values()
                                  if p['payload']['metadata']['book_id'] == str(book_id)]
                    print(f"DEBUG: Points for book {book_id}: {len(book_points)}")
                else:
                    print(f"DEBUG: All points: {len(qdrant_service.points)}")

            if not search_results:
                rag_logger.log_retrieval(
                    "No relevant chunks found for query",
                    {"query": query, "book_id": str(book_id) if book_id else "all books"}
                )
                return []

            # Convert search results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                chunk_id = result["chunk_id"]
                content = result["content"]
                metadata = result["metadata"]
                similarity_score = result["similarity_score"]

                citation = Citation(
                    chunk_id=chunk_id,
                    chapter=metadata.get("chapter"),
                    section=metadata.get("section"),
                    page_number=metadata.get("page_number")
                )

                retrieved_chunk = RetrievedChunk(
                    retrieval_id=chunk_id,  # Using chunk_id as retrieval_id for simplicity
                    query_id=None,  # Will be set by the calling function
                    chunk_id=chunk_id,
                    similarity_score=similarity_score,
                    content=content,
                    chapter=metadata.get("chapter"),
                    section=metadata.get("section"),
                    page_number=metadata.get("page_number"),
                    created_at=None  # Will be set by the calling function
                )

                retrieved_chunks.append(retrieved_chunk)

            rag_logger.log_retrieval(
                f"Retrieved {len(retrieved_chunks)} relevant chunks",
                {
                    "query": query,
                    "book_id": str(book_id) if book_id else "all books",
                    "retrieved_count": len(retrieved_chunks)
                }
            )

            return retrieved_chunks

        except Exception as e:
            rag_logger.log_error(
                LogCategory.RETRIEVAL,
                f"Error during retrieval: {str(e)}",
                {"query": query, "book_id": str(book_id) if book_id else "all books", "exception": str(e)},
                e
            )
            return []
    
    async def retrieve_from_selected_text(
        self, 
        query: str, 
        selected_text: str, 
        top_k: Optional[int] = None
    ) -> List[RetrievedChunk]:
        """
        Retrieve relevant content from user-selected text only.
        
        Args:
            query: The user's query
            selected_text: The text selected by the user
            top_k: Number of top results to return (defaults to settings.TOP_K)
            
        Returns:
            List of RetrievedChunk objects with content from selected text
        """
        if top_k is None:
            top_k = settings.TOP_K
            
        try:
            rag_logger.log_retrieval(
                "Starting retrieval for query in selected text",
                {"query": query, "selected_text_length": len(selected_text)}
            )
            
            # Generate embedding for the query
            query_embeddings = cohere_client.generate_embeddings([query])
            if not query_embeddings or len(query_embeddings) == 0:
                rag_logger.log_error(
                    LogCategory.RETRIEVAL,
                    "Failed to generate embedding for query",
                    {"query": query}
                )
                return []
            
            query_embedding = query_embeddings[0]
            
            # Search in Qdrant for content within the selected text
            search_results = qdrant_service.search_in_selected_text(
                query_embedding=query_embedding,
                selected_text=selected_text,
                top_k=top_k
            )
            
            # Convert search results to RetrievedChunk objects
            retrieved_chunks = []
            for result in search_results:
                content = result["content"]
                similarity_score = result["similarity_score"]
                
                # For selected text, we create a citation with source information
                citation = Citation(
                    chunk_id=None,  # No specific chunk ID for selected text
                    chapter="Selected Text",
                    section=None,
                    page_number=None
                )
                
                retrieved_chunk = RetrievedChunk(
                    retrieval_id=None,  # Will be generated
                    query_id=None,  # Will be set by the calling function
                    chunk_id=None,  # No specific chunk ID for selected text
                    similarity_score=similarity_score,
                    content=content,
                    chapter="Selected Text",
                    section=None,
                    page_number=None,
                    created_at=None  # Will be set by the calling function
                )
                
                retrieved_chunks.append(retrieved_chunk)
            
            rag_logger.log_retrieval(
                f"Retrieved {len(retrieved_chunks)} relevant chunks from selected text",
                {
                    "query": query,
                    "selected_text_length": len(selected_text),
                    "retrieved_count": len(retrieved_chunks)
                }
            )
            
            return retrieved_chunks
            
        except Exception as e:
            rag_logger.log_error(
                LogCategory.RETRIEVAL,
                f"Error during selected text retrieval: {str(e)}",
                {"query": query, "selected_text_length": len(selected_text) if selected_text else 0, "exception": str(e)},
                e
            )
            return []


# Global instance
retrieval_service = RetrievalService()