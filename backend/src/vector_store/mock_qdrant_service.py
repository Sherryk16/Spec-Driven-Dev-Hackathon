"""
Mock Qdrant Cloud integration for testing purposes.
Replaces actual Qdrant calls with in-memory storage.
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
import random


class MockQdrantService:
    def __init__(self):
        # In-memory storage for testing
        self.collection_name = "book_content_chunks"
        self.points = {}  # Dictionary to store embeddings with their IDs as keys
        print(f"Mock Qdrant service initialized with collection: {self.collection_name}")

    def store_embeddings(self,
                        book_id: UUID,
                        chunk_ids: List[UUID],
                        embeddings: List[List[float]],
                        chunk_contents: List[str],
                        metadata_list: List[Dict[str, Any]]) -> bool:
        """
        Store embeddings in mock Qdrant with metadata.

        Args:
            book_id: The ID of the book these chunks belong to
            chunk_ids: List of UUIDs for the chunks
            embeddings: List of embedding vectors
            chunk_contents: List of chunk text contents
            metadata_list: List of metadata dictionaries for each chunk

        Returns:
            True if successful, False otherwise
        """
        try:
            for chunk_id, embedding, content, metadata in zip(
                chunk_ids, embeddings, chunk_contents, metadata_list
            ):
                # Store the point data
                self.points[str(chunk_id)] = {
                    "vector": embedding,
                    "payload": {
                        "content": content,
                        "metadata": {
                            "book_id": str(book_id),
                            "chunk_id": str(chunk_id),
                            **metadata
                        }
                    }
                }

            print(f"Successfully stored {len(chunk_ids)} embeddings for book {book_id}")
            return True
        except Exception as e:
            print(f"Error storing embeddings in mock Qdrant: {e}")
            return False

    def search(self,
               query_embedding: List[float],
               book_id: Optional[UUID] = None,
               top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks in mock Qdrant using cosine similarity.

        Args:
            query_embedding: The embedding vector to search for
            book_id: Optional book ID to filter results to a specific book
            top_k: Number of top results to return

        Returns:
            List of dictionaries containing content, metadata, and similarity scores
        """
        try:
            results = []
            
            for point_id, point_data in self.points.items():
                # Filter by book_id if specified
                if book_id and point_data["payload"]["metadata"]["book_id"] != str(book_id):
                    continue
                
                # Calculate cosine similarity between query and stored embeddings
                similarity = self._cosine_similarity(query_embedding, point_data["vector"])
                
                result = {
                    "chunk_id": UUID(point_data["payload"]["metadata"]["chunk_id"]),
                    "content": point_data["payload"]["content"],
                    "metadata": point_data["payload"]["metadata"],
                    "similarity_score": similarity
                }
                
                results.append(result)
            
            # Sort results by similarity score in descending order
            results.sort(key=lambda x: x["similarity_score"], reverse=True)
            
            # Return top_k results
            return results[:top_k]
            
        except Exception as e:
            print(f"Error searching in mock Qdrant: {e}")
            return []

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        """
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        
        # Calculate magnitudes
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        
        # Ensure the similarity is between -1 and 1
        return max(-1.0, min(1.0, similarity))

    def search_in_selected_text(self,
                                query_embedding: List[float],
                                selected_text: str,
                                top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar content only within the selected text.
        This method creates a temporary search within the selected text context.

        Args:
            query_embedding: The embedding vector to search for
            selected_text: The text to search within
            top_k: Number of top results to return (will be 1 if only selected text is considered)

        Returns:
            List of dictionaries containing content, metadata, and similarity scores
        """
        # For selected text queries, we return the selected text itself
        # with a high similarity score since it's the exact text the user specified
        return [{
            "chunk_id": None,  # No specific chunk ID for selected text
            "content": selected_text,
            "metadata": {"source": "selected_text"},
            "similarity_score": 1.0
        }]


# Global mock instance to be used throughout the application
qdrant_service = MockQdrantService()