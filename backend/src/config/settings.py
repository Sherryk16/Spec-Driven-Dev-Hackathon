"""
Configuration settings for the Integrated RAG Chatbot.
All settings are loaded from environment variables.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Cohere settings
    COHERE_API_KEY: str = "dummy_key_for_testing"

    # Qdrant settings
    QDRANT_URL: str = "https://dummy-url.qdrant.io"
    QDRANT_API_KEY: str = "dummy_key_for_testing"
    QDRANT_CLUSTER_ID: str = "dummy_cluster_id"

    # Neon Postgres settings
    NEON_DATABASE_URL: str = "postgresql://dummy:dummy@dummy.neon.tech/dummy_db"
    
    # Application settings
    APP_NAME: str = "Integrated RAG Chatbot for Published Book"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # RAG settings
    CHUNK_SIZE: int = 512  # tokens
    CHUNK_OVERLAP: int = 64  # tokens
    TOP_K: int = 5
    MAX_BOOK_SIZE_PAGES: int = 1000
    MAX_BOOK_SIZE_CHARS: int = 50000000  # 50MB
    MAX_RESPONSE_TIME: float = 15.0  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()