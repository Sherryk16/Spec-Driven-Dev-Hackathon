<!--
Sync Impact Report:
- Version change: 0.1.0 → 1.0.0
- Modified principles: All 6 principles replaced with project-specific ones
- Added sections: Core Principles (6), Additional Constraints, Development Workflow
- Removed sections: None
- Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Integrated RAG Chatbot for Published Book Constitution

## Core Principles

### Faithfulness
Responses must strictly reflect the source book content. All generated answers must be based solely on the indexed book material without introducing external information or assumptions.

### Grounded Generation
No hallucinations or external knowledge beyond indexed data. The system must only generate responses based on retrieved document chunks that have been properly processed and stored in the vector database.

### Transparency
Every answer must be traceable to specific book passages. All responses must include citations or references to the specific sections, chapters, or pages from which the information was derived.

### Modularity
Clear separation of ingestion, retrieval, and generation layers. Each component must be independently developable, testable, and maintainable with well-defined interfaces between them.

### Scalability
Designed to support large books and multiple users. The architecture must handle increasing amounts of content and concurrent users without significant performance degradation.

### Security & Privacy
No user data leakage or unauthorized content access. All user interactions and data must be handled securely, with appropriate access controls and privacy protection measures.

## Additional Constraints

- No OpenAI SDKs, APIs, or dependencies: The system must exclusively use Cohere API for embeddings and generation
- Cohere API usage must be configurable via environment variables
- Embedding Model: Cohere embedding models only (no OpenAI usage)
- LLM Generation: Cohere generation models only
- Vector Store: Qdrant Cloud Free Tier
- Database: Neon Serverless Postgres
- Backend Framework: FastAPI
- Specification Tooling: SpeciKitPlus + Qwen CLI

## Development Workflow

- API Design: RESTful endpoints with clear request/response schemas
- Text Chunking: Deterministic chunking with overlap and metadata (chapter, page, section)
- RAG Behavior Rules: Answers must be generated only from retrieved chunks
- When relevant content is not found, respond with: "The selected book content does not contain enough information to answer this question."
- When user selects specific text, retrieval must be limited strictly to that selection
- No inference beyond explicitly stated text
- No external knowledge, training data, or assumptions

## Governance

This constitution governs all development decisions for the Integrated RAG Chatbot project. All implementations must comply with these principles. Amendments require documentation of the change, impact assessment, and approval by the project maintainers. All pull requests and code reviews must verify compliance with these principles. The development team must follow the specifications and plans derived from this constitution.

**Version**: 1.0.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-12-19
