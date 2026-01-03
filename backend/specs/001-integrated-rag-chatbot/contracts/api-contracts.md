# API Contracts: Integrated RAG Chatbot for Published Book

## Contract: POST /ingest/book

**Purpose**: Ingest a book file and process it for RAG queries

**Request**:
- Method: POST
- Path: /ingest/book
- Content-Type: multipart/form-data
- Body:
  - file: File (PDF, EPUB, or Text format)
  - metadata: JSON object containing:
    - title: String (book title)
    - author: String (book author)
    - book_id: String (optional, auto-generated if not provided)

**Response**:
- Success (200):
  ```json
  {
    "status": "success",
    "book_id": "uuid-string",
    "title": "book title",
    "chunks_processed": 120,
    "processing_time": "2.5s"
  }
  ```
- Error (400):
  ```json
  {
    "status": "error",
    "message": "Invalid file format or missing required fields"
  }
  ```
- Error (500):
  ```json
  {
    "status": "error",
    "message": "Internal server error during ingestion"
  }
  ```

## Contract: POST /chat/query

**Purpose**: Submit a question about the book content and receive an answer

**Request**:
- Method: POST
- Path: /chat/query
- Content-Type: application/json
- Body:
  ```json
  {
    "book_id": "uuid-string",
    "query": "What is the main theme of this book?",
    "session_id": "optional-uuid-string"
  }
  ```

**Response**:
- Success (200):
  ```json
  {
    "response_id": "uuid-string",
    "answer": "The main theme of this book is...",
    "citations": [
      {
        "chunk_id": "uuid-string",
        "chapter": "Chapter 3",
        "section": "Section 2",
        "page_number": 45
      }
    ],
    "query_time": "1.2s"
  }
  ```
- Error (400):
  ```json
  {
    "status": "error",
    "message": "Missing required fields or invalid book_id"
  }
  ```
- Success with fallback (200):
  ```json
  {
    "response_id": "uuid-string",
    "answer": "The provided book content does not contain sufficient information to answer this question.",
    "citations": [],
    "query_time": "0.8s"
  }
  ```

## Contract: POST /chat/query-selected-text

**Purpose**: Submit a question about user-selected text and receive an answer limited to that text

**Request**:
- Method: POST
- Path: /chat/query-selected-text
- Content-Type: application/json
- Body:
  ```json
  {
    "book_id": "uuid-string",
    "query": "What does this passage mean?",
    "selected_text": "The specific text selected by the user...",
    "session_id": "optional-uuid-string"
  }
  ```

**Response**:
- Success (200):
  ```json
  {
    "response_id": "uuid-string",
    "answer": "Based on the selected text, this passage means...",
    "citations": [
      {
        "chunk_id": "uuid-string",
        "chapter": "Chapter 3",
        "section": "Section 2",
        "page_number": 45
      }
    ],
    "query_time": "1.5s"
  }
  ```
- Error (400):
  ```json
  {
    "status": "error",
    "message": "Missing required fields, invalid book_id, or empty selected_text"
  }
  ```
- Success with fallback (200):
  ```json
  {
    "response_id": "uuid-string",
    "answer": "The provided book content does not contain sufficient information to answer this question.",
    "citations": [],
    "query_time": "0.9s"
  }
  ```

## Contract: GET /health

**Purpose**: Check the health status of the service

**Request**:
- Method: GET
- Path: /health

**Response**:
- Success (200):
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-12-19T10:30:00Z",
    "dependencies": {
      "cohere_api": "connected",
      "qdrant": "connected",
      "neon_postgres": "connected"
    }
  }
  ```
- Error (503):
  ```json
  {
    "status": "unhealthy",
    "timestamp": "2025-12-19T10:30:00Z",
    "dependencies": {
      "cohere_api": "disconnected",
      "qdrant": "connected",
      "neon_postgres": "connected"
    }
  }
  ```