---
id: 1
title: Create-Spec
stage: spec
date: 2025-12-19
surface: agent
model: Qwen
feature: integrated-rag-chatbot
branch: 001-integrated-rag-chatbot
user: user
command: /sp.specify
labels:
  - rag
  - chatbot
  - specification
  - cohere
links:
  - spec: specs/001-integrated-rag-chatbot/spec.md
  - ticket: null
  - adr: null
  - pr: null
files:
  - specs/001-integrated-rag-chatbot/spec.md
  - specs/001-integrated-rag-chatbot/checklists/requirements.md
tests:
  - null
---

# Create Spec for Integrated RAG Chatbot

## Prompt Text

Integrated RAG Chatbot for Published Book (Cohere + Qdrant) Target audience: * Readers of the published book * Developers embedding the chatbot into a book platform * Technical reviewers evaluating RAG correctness and faithfulness Objective: Specify and generate a production-ready Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly from the book's content, including support for queries restricted to user-selected text only. Technology Stack (Fixed): * LLM & Embeddings: Cohere API (mandatory, no OpenAI usage) * Backend: FastAPI (Python) * Vector Database: Qdrant Cloud (Free Tier) * Relational Database: Neon Serverless Postgres * Specification & Generation: SpeciKitPlus + Qwen CLI * Deployment: Free-tier compatible infrastructure Credentials & Configuration (Environment-Based): * QDRANT_URL = https://98c42b84-103c-4340-8527-bb0664e526c2.europe-west3-0.gcp.cloud.qdrant.io * QDRANT_API_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.oAxILQHgxRkGNAamHKdhLUInT_L4XJIAx7xcJC0w1aA * QDRANT_CLUSTER_ID = 98c42b84-103c-4340-8527-bb0664e526c2 * NEON_DATABASE_URL = postgresql://neondb_owner:npg_cWsdeSlzD5P8@ep-bitter-poetry-ad3xr58z-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require * COHERE_API_KEY = EPPNDjgG9w1MhdFaMVNaE2BMUUjw2zCpJ7keazXm ⚠️ No credentials may be hard-coded in source files or prompts. All secrets must be loaded via environment variables only. Functional Requirements: * Ingest book content (PDF/EPUB/Text) * Chunk text deterministically with overlap * Generate embeddings using Cohere embedding models * Store vectors in Qdrant with metadata: - book_id - chapter - section - page_number * Retrieve top-k relevant chunks for each query * Generate answers only from retrieved chunks * Support user-selected text queries with restricted retrieval scope RAG Rules (Hard Constraints): * No hallucinations or external knowledge * If answer not found in retrieved chunks, respond exactly: "The provided book content does not contain sufficient information to answer this question." * When text is selected by user: - Retrieval must be limited only to that text - No global book search allowed * Responses must be concise, factual, and grounded API Requirements: * POST /ingest/book * POST /chat/query * POST /chat/query-selected-text * GET /health * All endpoints must have explicit request/response schemas Success Criteria: * 100% answers grounded in book content * Zero external knowledge leakage * Deterministic and reproducible RAG pipeline * Fully operable on Qdrant + Neon free tiers * Entire system regenerable using SpeciKitPlus + Qwen CLI Constraints: * No OpenAI SDKs, APIs, or models * No fine-tuning of models * No web search or browsing * Stateless API design where possible * Clear logging and error handling Not Building: * General-purpose chatbot * Authoring or editing tools * Model fine-tuning pipelines * Analytics dashboards * Multi-book recommendation system Timeline Expectation: * Specification-driven generation in a single pass * Codebase structured for incremental extension Output Format: * Backend code (FastAPI) * Clear module separation (ingestion, retrieval, generation) * Configuration via environment variables * Ready for deployment

## Response Text

Successfully created the feature specification for the Integrated RAG Chatbot. The specification includes three user stories (P1: Query Book Content, P2: Query Selected Text, P3: Ingest New Book Content), functional requirements, key entities, and success criteria. All [NEEDS CLARIFICATION] markers were resolved with reasonable defaults. A quality checklist was also created and all items were marked as complete.

## Outcome

The specification is complete and ready for the next phase (planning). The feature branch '001-integrated-rag-chatbot' has been created with the spec file and quality checklist.