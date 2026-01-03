"""
Generation service for the Integrated RAG Chatbot.
Manages Cohere generation ensuring responses are grounded in retrieved content.
"""
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
# Try to import real services, fall back to mock if they fail
try:
    from src.services.cohere_service import cohere_client
except Exception:
    from src.services.mock_cohere_service import cohere_client
from src.models.api_models import RetrievedChunk, GeneratedResponse, Citation
from src.utils.logger import rag_logger, LogCategory
from src.config.settings import settings


class GenerationService:
    def __init__(self):
        pass
    
    async def generate_answer(
        self, 
        query: str, 
        retrieved_chunks: List[RetrievedChunk], 
        is_selected_text_query: bool = False
    ) -> GeneratedResponse:
        """
        Generate an answer based on the query and retrieved chunks.
        
        Args:
            query: The user's query
            retrieved_chunks: List of relevant chunks retrieved from the vector store
            is_selected_text_query: Whether this is a query on selected text only
            
        Returns:
            GeneratedResponse object with the answer and citations
        """
        try:
            query_id = uuid4()
            rag_logger.log_generation(
                "Starting response generation",
                {
                    "query": query,
                    "query_id": str(query_id),
                    "retrieved_chunks_count": len(retrieved_chunks),
                    "is_selected_text_query": is_selected_text_query
                }
            )
            
            # If no relevant chunks were found, return the fallback response
            if not retrieved_chunks or len(retrieved_chunks) == 0:
                fallback_response = "The provided book content does not contain sufficient information to answer this question."
                
                rag_logger.log_generation(
                    "No relevant chunks found, returning fallback response",
                    {"query": query, "query_id": str(query_id)}
                )
                
                return GeneratedResponse(
                    response_id=uuid4(),
                    query_id=query_id,
                    response_text=fallback_response,
                    citations=[],
                    is_fallback_response=True,
                    created_at=datetime.utcnow()
                )
            
            # Construct the context from retrieved chunks
            context_parts = []
            citations = []
            
            for chunk in retrieved_chunks:
                context_parts.append(f"Source: {chunk.content}")
                
                citation = Citation(
                    chunk_id=chunk.chunk_id,
                    chapter=chunk.chapter,
                    section=chunk.section,
                    page_number=chunk.page_number
                )
                citations.append(citation)
            
            context = "\n\n".join(context_parts)
            
            # Create the prompt for the LLM
            prompt = self._construct_prompt(query, context)
            
            # Generate the response using Cohere
            response_text = cohere_client.generate_response(prompt)
            
            # Ensure the response is grounded in the provided context
            # This is a basic check - in a production system, you might want more sophisticated validation
            if not self._is_response_groundedin_context(response_text, context):
                rag_logger.log_generation(
                    "Response may not be fully grounded in context, returning fallback",
                    {"query": query, "query_id": str(query_id), "response": response_text}
                )
                response_text = "The provided book content does not contain sufficient information to answer this question."
                citations = []
            
            rag_logger.log_generation(
                "Successfully generated response",
                {
                    "query": query,
                    "query_id": str(query_id),
                    "response_length": len(response_text),
                    "citations_count": len(citations)
                }
            )
            
            return GeneratedResponse(
                response_id=uuid4(),
                query_id=query_id,
                response_text=response_text,
                citations=citations,
                is_fallback_response="The provided book content does not contain sufficient information to answer this question." in response_text,
                created_at=datetime.utcnow()
            )
            
        except Exception as e:
            rag_logger.log_error(
                LogCategory.GENERATION,
                f"Error during response generation: {str(e)}",
                {"query": query, "exception": str(e)},
                e
            )
            
            # Return fallback response in case of error
            return GeneratedResponse(
                response_id=uuid4(),
                query_id=uuid4(), # Generate a new UUID for query_id in case of error
                response_text="The provided book content does not contain sufficient information to answer this question.",
                citations=[],
                is_fallback_response=True,
                created_at=datetime.utcnow()
            )
    
    def _construct_prompt(self, query: str, context: str) -> str:
        """
        Construct the prompt for the LLM with context and query.
        
        Args:
            query: The user's query
            context: The retrieved context
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
        Based on the following context, please answer the question. If the context does not contain sufficient information to answer the question, respond with exactly: "The provided book content does not contain sufficient information to answer this question."
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:
        """
        return prompt.strip()
    
    def _is_response_groundedin_context(self, response: str, context: str) -> bool:
        """
        Basic check to see if the response seems grounded in the context.
        This is a simple heuristic and should be enhanced for production use.
        
        Args:
            response: The generated response
            context: The provided context
            
        Returns:
            True if the response appears grounded, False otherwise
        """
        # Check if the response is the fallback message
        if "The provided book content does not contain sufficient information to answer this question." in response:
            return True
            
        # Basic check: if response is very short and doesn't seem to address the query, it might not be grounded
        if len(response.strip()) < 20:
            return False
            
        # Additional checks could be implemented here, such as:
        # - Semantic similarity between response and context
        # - Keyword matching between query and response
        # - More sophisticated NLP analysis
        
        return True


# Global instance
generation_service = GenerationService()