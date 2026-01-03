# Data Model: Integrated RAG Chatbot for Published Book

## Entity: BookContent
- **Fields**:
  - book_id: UUID (Primary Key)
  - title: String (max 500)
  - author: String (max 200)
  - content: Text (full book text)
  - file_path: String (path to source file)
  - created_at: DateTime
  - updated_at: DateTime
- **Relationships**: None
- **Validation rules**:
  - title and author required
  - content must be between 1000 and 50MB characters
- **State transitions**: None

## Entity: TextChunk
- **Fields**:
  - chunk_id: UUID (Primary Key)
  - book_id: UUID (Foreign Key to BookContent)
  - content: Text (chunked text)
  - chunk_index: Integer (position in book)
  - chapter: String (optional)
  - section: String (optional)
  - page_number: Integer (optional)
  - embedding_vector: Array (Cohere embedding vector)
  - created_at: DateTime
- **Relationships**:
  - Belongs to BookContent
- **Validation rules**:
  - content required and between 100 and 1000 tokens
  - book_id must reference existing BookContent
  - embedding_vector must match Cohere embedding dimensions
- **State transitions**: None

## Entity: UserQuery
- **Fields**:
  - query_id: UUID (Primary Key)
  - book_id: UUID (Foreign Key to BookContent)
  - query_text: Text (user's question)
  - selected_text: Text (optional, for selected-text queries)
  - created_at: DateTime
- **Relationships**:
  - Belongs to BookContent
- **Validation rules**:
  - query_text required and between 10 and 1000 characters
  - book_id must reference existing BookContent
- **State transitions**: None

## Entity: RetrievedChunk
- **Fields**:
  - retrieval_id: UUID (Primary Key)
  - query_id: UUID (Foreign Key to UserQuery)
  - chunk_id: UUID (Foreign Key to TextChunk)
  - similarity_score: Float (0.0 to 1.0)
  - created_at: DateTime
- **Relationships**:
  - Belongs to UserQuery
  - Belongs to TextChunk
- **Validation rules**:
  - query_id and chunk_id must reference existing records
  - similarity_score between 0.0 and 1.0
- **State transitions**: None

## Entity: GeneratedResponse
- **Fields**:
  - response_id: UUID (Primary Key)
  - query_id: UUID (Foreign Key to UserQuery)
  - response_text: Text (generated answer)
  - citations: JSON (list of chunk_ids used)
  - is_fallback_response: Boolean (true if using fallback message)
  - created_at: DateTime
- **Relationships**:
  - Belongs to UserQuery
- **Validation rules**:
  - query_id must reference existing UserQuery
  - response_text required if not fallback
  - citations must reference existing TextChunks
- **State transitions**: None

## Entity: UserSession
- **Fields**:
  - session_id: UUID (Primary Key)
  - user_id: UUID (optional, for tracking)
  - book_id: UUID (Foreign Key to BookContent)
  - created_at: DateTime
  - last_accessed: DateTime
- **Relationships**:
  - Belongs to BookContent
- **Validation rules**:
  - book_id must reference existing BookContent
- **State transitions**: None