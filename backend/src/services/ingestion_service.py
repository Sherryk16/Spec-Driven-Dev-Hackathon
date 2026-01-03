"""
Ingestion service for the Integrated RAG Chatbot.
Handles book ingestion, text extraction, and chunking.
"""
from typing import Optional, Tuple
import tempfile
import os
from pathlib import Path
from uuid import UUID
from pypdf import PdfReader
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import asyncio
from src.utils.text_chunker import text_chunker
# Try to import real services, fall back to mock if they fail
try:
    from src.services.cohere_service import cohere_client
    from src.vector_store.qdrant_service import qdrant_service
except Exception:
    from src.services.mock_cohere_service import cohere_client
    from src.vector_store.mock_qdrant_service import qdrant_service
from src.database.schemas import BookContentDB, TextChunkDB
from src.utils.logger import rag_logger, LogCategory
from src.config.settings import settings


class IngestionService:
    def __init__(self):
        pass
    
    async def ingest_book(self, file_path: str, book_id: UUID, title: str, author: str) -> Tuple[bool, int]:
        """
        Ingest a book file, extract text, chunk it, generate embeddings, and store in vector DB.
        
        Args:
            file_path: Path to the book file (PDF, EPUB, or text)
            book_id: UUID for the book
            title: Title of the book
            author: Author of the book
            
        Returns:
            Tuple of (success: bool, number of chunks processed: int)
        """
        try:
            # Extract text from the book file
            rag_logger.log_ingestion(f"Starting ingestion for book {title} by {author}")
            
            text_content = await self._extract_text(file_path)
            if not text_content:
                rag_logger.log_error(LogCategory.INGESTION,
                    f"Failed to extract text from {file_path}",
                    {"book_id": str(book_id), "file_path": file_path}
                )
                return False, 0
            
            # Chunk the text
            chunks_with_metadata = text_chunker.chunk_text(
                text=text_content,
                book_id=str(book_id),
                chapter="1",  # In a real implementation, this would come from the book structure
                section=None,
                page_number=None
            )
            
            if not chunks_with_metadata:
                rag_logger.log_error(LogCategory.INGESTION,
                    f"No chunks created from book content",
                    {"book_id": str(book_id), "title": title}
                )
                return False, 0
            
            # Extract just the text chunks for embedding
            chunk_texts = [chunk_text for chunk_text, _ in chunks_with_metadata]
            
            # Generate embeddings using Cohere
            rag_logger.log_embedding(f"Generating embeddings for {len(chunk_texts)} chunks")
            embeddings = cohere_client.generate_embeddings(chunk_texts)
            
            if len(embeddings) != len(chunk_texts):
                rag_logger.log_error(LogCategory.EMBEDDING,
                    "Mismatch between number of chunks and embeddings generated",
                    {
                        "book_id": str(book_id),
                        "chunks_count": len(chunk_texts),
                        "embeddings_count": len(embeddings)
                    }
                )
                return False, 0
            
            # Generate UUIDs for the chunks
            import uuid
            chunk_uuids = [uuid.uuid4() for _ in chunk_texts]

            success = qdrant_service.store_embeddings(
                book_id=book_id,
                chunk_ids=chunk_uuids,
                embeddings=embeddings,
                chunk_contents=chunk_texts,
                metadata_list=[metadata for _, metadata in chunks_with_metadata]
            )
            
            if success:
                rag_logger.log_ingestion(
                    f"Successfully ingested book {title}",
                    {
                        "book_id": str(book_id),
                        "chunks_processed": len(chunk_texts),
                        "title": title
                    }
                )
                return True, len(chunk_texts)
            else:
                rag_logger.log_error(LogCategory.INGESTION,
                    f"Failed to store embeddings in Qdrant for book {title}",
                    {"book_id": str(book_id), "title": title}
                )
                return False, 0
                
        except Exception as e:
            rag_logger.log_error(LogCategory.INGESTION,
                f"Error during book ingestion: {str(e)}",
                {"book_id": str(book_id), "file_path": file_path, "exception": str(e)},
                e
            )
            return False, 0
    
    async def _extract_text(self, file_path: str) -> Optional[str]:
        """
        Extract text from a book file based on its format.
        
        Args:
            file_path: Path to the book file
            
        Returns:
            Extracted text content or None if extraction failed
        """
        file_extension = Path(file_path).suffix.lower()
        
        try:
            if file_extension == '.pdf':
                try:
                    return await self._extract_text_from_pdf(file_path)
                except Exception as pdf_e:
                    rag_logger.log_error(LogCategory.INGESTION,
                        f"PDF extraction failed for {file_path}, attempting to read as text. Error: {str(pdf_e)}",
                        {"file_path": file_path, "exception": str(pdf_e)}
                    )
                    # Fallback to reading as text if PDF extraction fails
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        return file.read()
            elif file_extension in ['.epub', '.mobi', '.azw', '.azw3']:
                return await self._extract_text_from_epub(file_path)
            elif file_extension in ['.txt', '.text']:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            else:
                # For unsupported formats, try to read as text
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    return file.read()
        except Exception as e:
            rag_logger.log_error(LogCategory.INGESTION,
                f"Error extracting text from {file_path}",
                {"file_path": file_path, "exception": str(e)},
                e
            )
            return None
    
    async def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        text_parts = []
        
        try:
            reader = PdfReader(file_path)
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    text_parts.append(text)
                    
        except Exception as e:
            rag_logger.log_error(LogCategory.INGESTION,
                f"Error reading PDF {file_path}",
                {"file_path": file_path, "exception": str(e)},
                e
            )
            return "" # Return empty string on PDF read error
        
        return "\n".join(text_parts)
    
    async def _extract_text_from_epub(self, file_path: str) -> str:
        """Extract text from an EPUB file."""
        text_parts = []
        
        try:
            # Create a temporary directory to extract the EPUB
            with tempfile.TemporaryDirectory() as temp_dir:
                # EPUB is a ZIP file with specific structure
                import zipfile
                with zipfile.ZipFile(file_path, 'r') as epub_zip:
                    epub_zip.extractall(temp_dir)
                
                # Look for content files in the extracted EPUB
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(('.xhtml', '.html', '.htm', '.xml')):
                            file_path_full = os.path.join(root, file)
                            try:
                                with open(file_path_full, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    soup = BeautifulSoup(content, 'html.parser')
                                    text = soup.get_text()
                                    if text.strip():
                                        text_parts.append(text)
                            except Exception as e:
                                rag_logger.log_error(
                                    LogCategory.INGESTION,
                                    f"Error reading EPUB content file {file_path_full}",
                                    {"exception": str(e)},

                                    e
                                )
        except Exception as e:
            rag_logger.log_error(LogCategory.INGESTION,
                f"Error extracting EPUB {file_path}",
                {"file_path": file_path, "exception": str(e)},
                e
            )
        
        return "\n".join(text_parts)


# Global instance
ingestion_service = IngestionService()