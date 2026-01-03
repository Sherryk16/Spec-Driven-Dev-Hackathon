"""
Structured logging for the Integrated RAG Chatbot system.
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any
from enum import Enum


class LogCategory(Enum):
    INGESTION = "ingestion"
    EMBEDDING = "embedding"
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    API = "api"
    SYSTEM = "system"


class RAGLogger:
    def __init__(self, name: str = "rag_chatbot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create handler if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log_structured(self, level: int, category: LogCategory, message: str, 
                       extra_data: Dict[str, Any] = None):
        """Log a structured message with category and extra data."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "category": category.value,
            "message": message
        }
        
        if extra_data:
            log_data.update(extra_data)
        
        self.logger.log(level, json.dumps(log_data))
    
    def log_ingestion(self, message: str, extra_data: Dict[str, Any] = None):
        """Log ingestion-related events."""
        self._log_structured(logging.INFO, LogCategory.INGESTION, message, extra_data)
    
    def log_embedding(self, message: str, extra_data: Dict[str, Any] = None):
        """Log embedding-related events."""
        self._log_structured(logging.INFO, LogCategory.EMBEDDING, message, extra_data)
    
    def log_retrieval(self, message: str, extra_data: Dict[str, Any] = None):
        """Log retrieval-related events."""
        self._log_structured(logging.INFO, LogCategory.RETRIEVAL, message, extra_data)
    
    def log_generation(self, message: str, extra_data: Dict[str, Any] = None):
        """Log generation-related events."""
        self._log_structured(logging.INFO, LogCategory.GENERATION, message, extra_data)
    
    def log_api(self, message: str, extra_data: Dict[str, Any] = None):
        """Log API-related events."""
        self._log_structured(logging.INFO, LogCategory.API, message, extra_data)
    
    def log_error(self, category: LogCategory, message: str,
                  extra_data: Dict[str, Any] = None, exception: Exception = None):
        """Log error events."""
        error_data = extra_data or {}
        if exception:
            error_data["exception"] = str(exception)
            error_data["exception_type"] = type(exception).__name__

        self._log_structured(logging.ERROR, category, message, error_data)
    
    def log_system(self, message: str, extra_data: Dict[str, Any] = None):
        """Log system-related events."""
        self._log_structured(logging.INFO, LogCategory.SYSTEM, message, extra_data)


# Global logger instance
rag_logger = RAGLogger()