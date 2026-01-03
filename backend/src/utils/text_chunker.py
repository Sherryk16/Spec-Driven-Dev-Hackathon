"""
Text chunking logic for the Integrated RAG Chatbot.
Implements deterministic chunking with overlap and metadata preservation.
"""
import re
from typing import List, Tuple, Optional
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import tiktoken  # Alternative tokenizer if tokenizers library is not available


class TextChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 64):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size: Target size of each chunk in tokens
            overlap: Number of overlapping tokens between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        # Using tiktoken's cl100k_base tokenizer which is suitable for most use cases
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text."""
        return len(self.tokenizer.encode(text))
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Split text into sentences to preserve semantic boundaries."""
        # Split by sentence endings, preserving the delimiters
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Clean up any empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def chunk_text(self, 
                   text: str, 
                   book_id: str, 
                   chapter: Optional[str] = None, 
                   section: Optional[str] = None, 
                   page_number: Optional[int] = None) -> List[Tuple[str, dict]]:
        """
        Chunk the provided text into overlapping segments with metadata.
        
        Args:
            text: The text to chunk
            book_id: ID of the book this text belongs to
            chapter: Chapter name/number (optional)
            section: Section name (optional)
            page_number: Page number (optional)
            
        Returns:
            List of tuples containing (chunk_text, metadata_dict)
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Split text into sentences to preserve semantic boundaries
        sentences = self._split_by_sentences(text)
        if not sentences:
            return []
        
        chunks = []
        current_chunk = ""
        current_tokens = 0
        chunk_index = 0
        
        i = 0
        while i < len(sentences):
            sentence = sentences[i]
            sentence_tokens = self._count_tokens(sentence)
            
            # If adding this sentence would exceed chunk size
            if current_tokens + sentence_tokens > self.chunk_size and current_chunk:
                # Save the current chunk
                chunks.append((current_chunk.strip(), {
                    "book_id": book_id,
                    "chunk_index": chunk_index,
                    "chapter": chapter,
                    "section": section,
                    "page_number": page_number
                }))
                
                # Start a new chunk with overlap
                if self.overlap > 0:
                    # Find the last 'overlap' tokens worth of text from the current chunk
                    chunk_tokens = self.tokenizer.encode(current_chunk)
                    overlap_tokens = chunk_tokens[-self.overlap:]
                    overlap_text = self.tokenizer.decode(overlap_tokens)
                    
                    current_chunk = overlap_text + " " + sentence
                    current_tokens = self._count_tokens(current_chunk)
                else:
                    current_chunk = sentence
                    current_tokens = sentence_tokens
                
                chunk_index += 1
                i += 1
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_tokens += sentence_tokens
                i += 1
        
        # Add the final chunk if it has content
        if current_chunk.strip():
            chunks.append((current_chunk.strip(), {
                "book_id": book_id,
                "chunk_index": chunk_index,
                "chapter": chapter,
                "section": section,
                "page_number": page_number
            }))
        
        return chunks


# Global instance
text_chunker = TextChunker()