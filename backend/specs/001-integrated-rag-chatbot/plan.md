# Implementation Plan: Integrated RAG Chatbot for Published Book

**Branch**: `001-integrated-rag-chatbot` | **Date**: 2025-12-19 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-integrated-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Integrated RAG Chatbot will be a production-ready system that answers questions strictly from book content, with support for queries restricted to user-selected text. The system will use Cohere API for embeddings and generation, FastAPI for backend services, Qdrant Cloud for vector storage, and Neon Serverless Postgres for metadata. The architecture will follow a clean separation of concerns with ingestion, retrieval, and generation layers.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, Cohere, Qdrant, Neon Postgres, Pydantic, SQLAlchemy
**Storage**: Qdrant Cloud (vector storage), Neon Serverless Postgres (metadata)
**Testing**: pytest with specific RAG validation tests
**Target Platform**: Cloud server (compatible with free-tier resources)
**Project Type**: Backend API service
**Performance Goals**: 95% of queries return relevant answers within 15 seconds
**Constraints**: Must operate within Qdrant Cloud Free Tier and Neon Serverless limits, no OpenAI dependencies
**Scale/Scope**: Support books up to 1000 pages or 50MB

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The following checks ensure compliance with the Integrated RAG Chatbot Constitution:

- **Faithfulness**: Implementation must ensure responses strictly reflect source book content
- **Grounded Generation**: No hallucinations or external knowledge beyond indexed data allowed
- **Transparency**: Every answer must be traceable to specific book passages with citations
- **Modularity**: Clear separation of ingestion, retrieval, and generation layers required
- **Scalability**: Architecture must support large books and multiple concurrent users
- **Security & Privacy**: Implementation must prevent user data leakage and unauthorized access
- **Technology Stack**: Must use Cohere API (not OpenAI), Qdrant Cloud, Neon Postgres, FastAPI
- **RAG Behavior**: Answers must be generated only from retrieved chunks with proper fallback responses

## Project Structure

### Documentation (this feature)

```text
specs/001-integrated-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/              # Pydantic models for API requests/responses
│   ├── book_content.py  # Book content models
│   ├── user_query.py    # User query models
│   └── response.py      # Response models with citations
├── services/            # Business logic services
│   ├── ingestion_service.py    # Handles book ingestion and chunking
│   ├── embedding_service.py    # Manages Cohere embeddings
│   ├── retrieval_service.py    # Handles vector search in Qdrant
│   └── generation_service.py   # Manages Cohere generation
├── api/                 # FastAPI route definitions
│   ├── main.py          # Main app definition
│   ├── ingest.py        # Ingestion endpoints
│   ├── chat.py          # Chat/query endpoints
│   └── health.py        # Health check endpoint
├── database/            # Database interactions
│   ├── postgres.py      # Neon Postgres connection
│   └── schemas.py       # SQLAlchemy schemas
├── vector_store/        # Qdrant interactions
│   ├── qdrant_client.py # Qdrant client configuration
│   └── collection.py    # Collection management
├── config/              # Configuration management
│   └── settings.py      # Settings from environment variables
└── utils/               # Utility functions
    ├── text_chunker.py  # Text chunking logic
    ├── validators.py    # Input validation
    └── logger.py        # Structured logging
```

**Structure Decision**: Single project backend API service with clear separation of concerns following the RAG architecture (ingestion → embedding → retrieval → generation). The modular structure allows each component to be independently testable and maintainable.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All requirements align with constitution] |