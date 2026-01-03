"""
Qdrant Cloud integration for the Integrated RAG Chatbot vector storage.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Optional, Dict, Any
from uuid import UUID
import numpy as np
from src.config.settings import settings


class QdrantService:
    def __init__(self):
        # Initialize Qdrant client with cloud settings
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            # Use HTTPS and specify the cluster ID if needed
        )
        
        # Define collection name
        self.collection_name = "book_content_chunks"
        
        # Create collection if it doesn't exist
        self._create_collection()
    
    def _create_collection(self):
        """Create the Qdrant collection if it doesn't exist."""
        # Check if collection already exists
        existing_collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in existing_collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere's multilingual embedding dimension
                    distance=models.Distance.COSINE
                )
            )
            
            # Create payload index for efficient filtering
            self.client.create_payload_index(
                collection_name=self.collection_name,
                field_name="book_id",
                field_schema=models.PayloadSchemaType.KEYWORD
            )
        else:
            print(f"Collection '{self.collection_name}' already exists, skipping creation.")
    
    def store_embeddings(self, 
                        book_id: UUID, 
                        chunk_ids: List[UUID], 
                        embeddings: List[List[float]], 
                        chunk_contents: List[str],
                        metadata_list: List[Dict[str, Any]]) -> bool:
        """
        Store embeddings in Qdrant with metadata.
        
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
            points = []
            for i, (chunk_id, embedding, content, metadata) in enumerate(
                zip(chunk_ids, embeddings, chunk_contents, metadata_list)
            ):
                # Add book_id to metadata for filtering
                point_metadata = {
                    "book_id": str(book_id),
                    "chunk_id": str(chunk_id),
                    **metadata  # Include other metadata like chapter, section, page_number
                }
                
                points.append(
                    models.PointStruct(
                        id=str(chunk_id),
                        vector=embedding,
                        payload={
                            "content": content,
                            "metadata": point_metadata
                        }
                    )
                )
            
            # Upload points to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            return True
        except Exception as e:
            print(f"Error storing embeddings in Qdrant: {e}")
            return False
    
    def search(self, 
               query_embedding: List[float], 
               book_id: Optional[UUID] = None, 
               top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar chunks in Qdrant.
        
        Args:
            query_embedding: The embedding vector to search for
            book_id: Optional book ID to filter results to a specific book
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries containing content, metadata, and similarity scores
        """
        try:
            # Prepare filters if book_id is specified
            filters = None
            if book_id:
                filters = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="payload.metadata.book_id",
                            match=models.MatchValue(value=str(book_id))
                        )
                    ]
                )
            
            # Perform search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=filters,
                limit=top_k
            )
            
            # Format results
            results = []
            for hit in search_results:
                result = {
                    "chunk_id": UUID(hit.payload["metadata"]["chunk_id"]),
                    "content": hit.payload["content"],
                    "metadata": hit.payload["metadata"],
                    "similarity_score": hit.score
                }
                results.append(result)
            
            return results
        except Exception as e:
            print(f"Error searching in Qdrant: {e}")
            return []
    
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


# Global instance to be used throughout the application
qdrant_service = QdrantService()