"""
Cohere API integration for the Integrated RAG Chatbot.
Ensures no OpenAI dependencies are used.
"""
import cohere
from typing import List, Tuple
from src.config.settings import settings


class CohereClient:
    def __init__(self):
        self.client = cohere.Client(settings.COHERE_API_KEY)
        # Using a model that works with various Cohere client versions
        self.embed_model = "small"  # Using a simpler model that's more widely supported
        self.generate_model = "command-r-plus"  # Using Cohere's generation model
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for the provided texts using Cohere API.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        # Try the embed function without input_type first (for older Cohere versions)
        try:
            response = self.client.embed(
                texts=texts,
                model=self.embed_model
            )
            return [embedding for embedding in response.embeddings]
        except Exception as e:
            # If that fails, try with a supported input_type
            try:
                response = self.client.embed(
                    texts=texts,
                    model=self.embed_model,
                    input_type="search_document"
                )
                return [embedding for embedding in response.embeddings]
            except Exception:
                # If both fail, raise the original exception
                raise e
    
    def generate_response(self, prompt: str, max_tokens: int = 300) -> str:
        """
        Generate a response using Cohere's language model.
        
        Args:
            prompt: The input prompt for generation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response
        """
        response = self.client.generate(
            model=self.generate_model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.3,  # Lower temperature for more consistent, factual responses
            stop_sequences=["\n\n"]  # Stop at double newlines to avoid rambling
        )
        
        if response.generations:
            return response.generations[0].text.strip()
        else:
            return ""
    
    def rerank(self, query: str, documents: List[str], top_n: int = 5) -> List[Tuple[int, str, float]]:
        """
        Rerank documents based on relevance to the query.
        
        Args:
            query: The search query
            documents: List of documents to rerank
            top_n: Number of top results to return
            
        Returns:
            List of tuples (index, document, relevance_score) sorted by relevance
        """
        response = self.client.rerank(
            model="rerank-multilingual-v2.0",
            query=query,
            documents=documents,
            top_n=top_n
        )
        
        return [(r.index, r.document["text"], r.relevance_score) for r in response.results]


# Global instance to be used throughout the application
cohere_client = CohereClient()