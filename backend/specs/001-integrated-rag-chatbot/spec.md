# Feature Specification: Integrated RAG Chatbot for Published Book

**Feature Branch**: `001-integrated-rag-chatbot`
**Created**: 2025-12-19
**Status**: Draft
**Input**: User description: "Integrated RAG Chatbot for Published Book (Cohere + Qdrant) Target audience: * Readers of the published book * Developers embedding the chatbot into a book platform * Technical reviewers evaluating RAG correctness and faithfulness Objective: Specify and generate a production-ready Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly from the book's content, including support for queries restricted to user-selected text only. Technology Stack (Fixed): * LLM & Embeddings: Cohere API (mandatory, no OpenAI usage) * Backend: FastAPI (Python) * Vector Database: Qdrant Cloud (Free Tier) * Relational Database: Neon Serverless Postgres * Specification & Generation: SpeciKitPlus + Qwen CLI * Deployment: Free-tier compatible infrastructure Credentials & Configuration (Environment-Based): * QDRANT_URL = https://98c42b84-103c-4340-8527-bb0664e526c2.europe-west3-0.gcp.cloud.qdrant.io * QDRANT_API_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.oAxILQHgxRkGNAamHKdhLUInT_L4XJIAx7xcJC0w1aA * QDRANT_CLUSTER_ID = 98c42b84-103c-4340-8527-bb0664e526c2 * NEON_DATABASE_URL = postgresql://neondb_owner:npg_cWsdeSlzD5P8@ep-bitter-poetry-ad3xr58z-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require * COHERE_API_KEY = EPPNDjgG9w1MhdFaMVNaE2BMUUjw2zCpJ7keazXm ⚠️ No credentials may be hard-coded in source files or prompts. All secrets must be loaded via environment variables only. Functional Requirements: * Ingest book content (PDF/EPUB/Text) * Chunk text deterministically with overlap * Generate embeddings using Cohere embedding models * Store vectors in Qdrant with metadata: - book_id - chapter - section - page_number * Retrieve top-k relevant chunks for each query * Generate answers only from retrieved chunks * Support user-selected text queries with restricted retrieval scope RAG Rules (Hard Constraints): * No hallucinations or external knowledge * If answer not found in retrieved chunks, respond exactly: "The provided book content does not contain sufficient information to answer this question." * When text is selected by user: - Retrieval must be limited only to that text - No global book search allowed * Responses must be concise, factual, and grounded API Requirements: * POST /ingest/book * POST /chat/query * POST /chat/query-selected-text * GET /health * All endpoints must have explicit request/response schemas Success Criteria: * 100% answers grounded in book content * Zero external knowledge leakage * Deterministic and reproducible RAG pipeline * Fully operable on Qdrant + Neon free tiers * Entire system regenerable using SpeciKitPlus + Qwen CLI Constraints: * No OpenAI SDKs, APIs, or models * No fine-tuning of models * No web search or browsing * Stateless API design where possible * Clear logging and error handling Not Building: * General-purpose chatbot * Authoring or editing tools * Model fine-tuning pipelines * Analytics dashboards * Multi-book recommendation system Timeline Expectation: * Specification-driven generation in a single pass * Codebase structured for incremental extension Output Format: * Backend code (FastAPI) * Clear module separation (ingestion, retrieval, generation) * Configuration via environment variables * Ready for deployment"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Query Book Content (Priority: P1)

As a reader of a published book, I want to ask questions about the book content so that I can quickly find specific information without manually searching through the text.

**Why this priority**: This is the core functionality that provides the primary value of the RAG chatbot - enabling users to ask questions and get accurate answers from the book content.

**Independent Test**: Can be fully tested by submitting a question about the book content and verifying that the response is grounded in the actual book text with proper citations.

**Acceptance Scenarios**:

1. **Given** a book has been successfully ingested and indexed, **When** a user submits a question about the book content, **Then** the system returns an accurate answer based only on the book content with citations to specific passages.

2. **Given** a user submits a question that cannot be answered with the book content, **When** the system processes the query, **Then** the system responds with exactly: "The provided book content does not contain sufficient information to answer this question."

3. **Given** a book has been ingested and indexed, **When** a user submits a question with ambiguous references, **Then** the system returns the most relevant answer based on the book content with proper citations.

---

### User Story 2 - Query Selected Text (Priority: P2)

As a reader who has selected specific text in the book, I want to ask questions limited to that text selection so that I can get focused answers without interference from the broader book content.

**Why this priority**: This provides a more advanced feature that allows users to constrain their queries to specific passages, which is essential for detailed analysis of particular sections.

**Independent Test**: Can be fully tested by selecting specific text in a book, asking a question about that text, and verifying that the response is limited to information from the selected text only.

**Acceptance Scenarios**:

1. **Given** a user has selected specific text in the book, **When** the user submits a question about that text, **Then** the system returns an answer based only on the selected text with proper citations.

2. **Given** a user has selected specific text in the book, **When** the user submits a question that cannot be answered with the selected text, **Then** the system responds with exactly: "The provided book content does not contain sufficient information to answer this question."

3. **Given** a user has selected text in the book, **When** the user submits a question that could be answered using other parts of the book, **Then** the system returns an answer based only on the selected text, not the broader book content.

---

### User Story 3 - Ingest New Book Content (Priority: P3)

As a developer embedding the chatbot into a book platform, I want to ingest new book content so that the RAG system can answer questions about that book.

**Why this priority**: This is the foundational capability that enables the system to work with different books, though it's lower priority than the query functionality since it's primarily an administrative task.

**Independent Test**: Can be fully tested by uploading a book file and verifying that it's properly processed, chunked, and indexed in the vector database.

**Acceptance Scenarios**:

1. **Given** a book file in PDF/EPUB/Text format, **When** the ingestion process is initiated, **Then** the book content is properly parsed, chunked with overlap, and stored in the vector database with appropriate metadata.

2. **Given** a book file with structured content (chapters, sections, pages), **When** the ingestion process runs, **Then** the metadata (book_id, chapter, section, page_number) is preserved and associated with the vector embeddings.

3. **Given** an already ingested book, **When** the ingestion process is run again, **Then** the system either updates the existing content or provides an appropriate error message.

---

### Edge Cases

- What happens when a user submits a query that contains personally identifiable information or sensitive content?
- How does the system handle extremely long books that might exceed memory or storage limitations?
- What happens when the Cohere API or Qdrant Cloud service is temporarily unavailable?
- How does the system handle books in languages that the Cohere model may not support well?
- What happens when the book contains tables, images, or other non-text elements?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST ingest book content from PDF, EPUB, or Text file formats
- **FR-002**: System MUST chunk text deterministically with configurable overlap to ensure consistent retrieval
- **FR-003**: System MUST generate embeddings using Cohere embedding models (no OpenAI usage allowed)
- **FR-004**: System MUST store vectors in Qdrant Cloud with metadata (book_id, chapter, section, page_number)
- **FR-005**: System MUST retrieve top-k relevant chunks for each query using vector similarity search
- **FR-006**: System MUST generate answers only from retrieved chunks without hallucinations
- **FR-007**: System MUST support user-selected text queries with restricted retrieval scope
- **FR-008**: System MUST respond with "The provided book content does not contain sufficient information to answer this question" when relevant content is not found
- **FR-009**: System MUST provide explicit request/response schemas for all API endpoints
- **FR-010**: System MUST ensure all responses are grounded in the book content with proper citations
- **FR-011**: System MUST implement POST /ingest/book endpoint for book ingestion
- **FR-012**: System MUST implement POST /chat/query endpoint for general book queries
- **FR-013**: System MUST implement POST /chat/query-selected-text endpoint for selected text queries
- **FR-014**: System MUST implement GET /health endpoint for system health checks
- **FR-015**: System MUST load all credentials via environment variables (no hardcoding allowed)
- **FR-016**: System MUST implement stateless API design where possible
- **FR-017**: System MUST provide clear logging and error handling for all operations

*Example of marking unclear requirements:*

- **FR-018**: System MUST support books up to 1000 pages or 50MB - based on standard book length and free-tier resource constraints
- **FR-019**: System MUST return responses within 15 seconds - balancing user experience with RAG processing requirements

### Key Entities *(include if feature involves data)*

- **BookContent**: Represents the ingested book content, including the original text, metadata (book_id, chapter, section, page_number), and vector embeddings
- **UserQuery**: Represents a user's question about the book content, including the query text and any selected text constraints
- **RetrievedChunk**: Represents a segment of book content retrieved by the vector search, including the text content and metadata for citation purposes
- **GeneratedResponse**: Represents the final answer generated by the system, including the response text and citations to specific book passages

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of responses are grounded in actual book content with proper citations to specific passages
- **SC-002**: Zero external knowledge leakage occurs - all answers are based solely on indexed book content
- **SC-003**: The system successfully processes and indexes books of various formats (PDF, EPUB, Text) without data loss
- **SC-004**: 95% of user queries return relevant answers within 15 seconds
- **SC-005**: The system operates reliably on Qdrant Cloud Free Tier and Neon Serverless Postgres without exceeding resource limits
- **SC-006**: The entire system can be regenerated using SpeciKitPlus + Qwen CLI following specification-driven development principles
- **SC-007**: 100% of user-selected text queries return answers based only on the selected text, not the broader book content
- **SC-008**: 99% of health check requests return success status