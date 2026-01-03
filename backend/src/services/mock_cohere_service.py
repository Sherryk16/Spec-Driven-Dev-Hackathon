"""
Mock Cohere API integration for testing purposes.
Replaces actual Cohere API calls with mock functionality.
"""
import random
from typing import List, Tuple
from src.config.settings import settings


class MockCohereClient:
    def __init__(self):
        # Using a mock approach for testing
        self.embed_model = "mock-embedding-model"
        self.generate_model = "mock-generation-model"

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate mock embeddings for the provided texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        # Generate consistent mock embeddings based on text content
        embeddings = []
        for text in texts:
            # Create a deterministic mock embedding based on text content
            # Using a simple hash-based approach to generate consistent vectors
            text_hash = hash(text) % (10 ** 8)  # Get a hash value
            
            # Generate a 1024-dimensional vector (Cohere's typical embedding size)
            embedding = []
            for i in range(1024):
                # Use the hash and position to generate pseudo-random values
                val = ((text_hash * (i + 1)) % 10000) / 10000.0
                embedding.append(val)
            
            embeddings.append(embedding)
        
        return embeddings

    def generate_response(self, prompt: str, max_tokens: int = 300) -> str:
        """
        Generate a mock response using a simple template approach.

        Args:
            prompt: The input prompt for generation
            max_tokens: Maximum number of tokens to generate (ignored in mock)

        Returns:
            Generated text response
        """
        # Simple response generation based on the prompt
        prompt_lower = prompt.lower()
        
        if "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello! I'm your AI assistant for robotics and AI topics. How can I help you today?"
        elif "robot" in prompt_lower:
            return "Robots are programmable machines that can perform tasks autonomously or semi-autonomously. They are widely used in manufacturing, healthcare, and research applications."
        elif "ai" in prompt_lower or "artificial intelligence" in prompt_lower:
            return "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents'."
        elif "ros" in prompt_lower:
            return "ROS (Robot Operating System) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior."
        elif "qdrant" in prompt_lower:
            return "Qdrant is a vector similarity search engine that provides a production-ready solution for high-dimensional vector search."
        else:
            # Default response for unknown queries
            return f"I understand you're asking about '{prompt[:50]}...'. I'm a mock assistant, so I can't provide detailed answers. In a real implementation, I would search through the ingested book content to provide an accurate response based on the provided text."

    def rerank(self, query: str, documents: List[str], top_n: int = 5) -> List[Tuple[int, str, float]]:
        """
        Mock rerank function that returns documents with mock relevance scores.

        Args:
            query: The search query
            documents: List of documents to rerank
            top_n: Number of top results to return

        Returns:
            List of tuples (index, document, relevance_score) sorted by relevance
        """
        # Return documents with mock relevance scores
        results = []
        for i, doc in enumerate(documents[:top_n]):
            # Generate a mock relevance score based on similarity to query
            score = random.random()  # Random score between 0 and 1
            results.append((i, doc, score))
        
        # Sort by relevance score in descending order
        results.sort(key=lambda x: x[2], reverse=True)
        return results


# Global mock instance to be used throughout the application
cohere_client = MockCohereClient()