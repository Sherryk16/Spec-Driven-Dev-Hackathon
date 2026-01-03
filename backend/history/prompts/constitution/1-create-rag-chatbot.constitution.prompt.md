---
id: 1
title: Create-RAG-Chatbot
stage: constitution
date: 2025-12-19
surface: agent
model: Qwen
feature: Integrated RAG Chatbot for Published Book
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - rag
  - chatbot
  - cohere
links:
  - spec: null
  - ticket: null
  - adr: null
  - pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - null
---

# Create RAG Chatbot Constitution

## Prompt Text

Project: Integrated RAG Chatbot for Published Book (Cohere-based)

Overview:
Build and embed a Retrieval-Augmented Generation (RAG) chatbot inside a published book platform. 
The chatbot must answer user questions strictly based on the book's content, including the ability 
to respond only using user-selected text passages. The system will use Cohere API for embeddings 
and generation, FastAPI for backend services, Neon Serverless Postgres for metadata and user state, 
Qdrant Cloud (Free Tier) for vector storage, and Qwen CLI + SpeciKitPlus for specification-driven development.

Core Principles:
- Faithfulness: Responses must strictly reflect the source book content
- Grounded Generation: No hallucinations or external knowledge beyond indexed data
- Transparency: Every answer must be traceable to specific book passages
- Modularity: Clear separation of ingestion, retrieval, and generation layers
- Scalability: Designed to support large books and multiple users
- Security & Privacy: No user data leakage or unauthorized content access

Key Standards:
- Embedding Model: Cohere embedding models only (no OpenAI usage)
- LLM Generation: Cohere generation models only
- Vector Store: Qdrant Cloud Free Tier
- Database: Neon Serverless Postgres
- Backend Framework: FastAPI
- Specification Tooling: SpeciKitPlus + Qwen CLI
- API Design: RESTful endpoints with clear request/response schemas
- Text Chunking: Deterministic chunking with overlap and metadata (chapter, page, section)

RAG Behavior Rules:
- Answers must be generated only from retrieved chunks
- If relevant content is not found, respond with:
  "The selected book content does not contain enough information to answer this question."
- When user selects specific text, retrieval must be limited strictly to that selection
- No inference beyond explicitly stated text
- No external knowledge, training data, or assumptions

Constraints:
- No OpenAI SDKs, APIs, or dependencies
- Cohere API usage must be configurable via environment variables

## Response Text

Successfully created and updated the project constitution for the Integrated RAG Chatbot for Published Book project with version 1.0.0. The constitution includes 6 core principles: Faithfulness, Grounded Generation, Transparency, Modularity, Scalability, and Security & Privacy. The dependent templates were also updated to align with the new constitution.

## Outcome

The constitution was successfully created with all specified principles and constraints. The dependent templates were updated to ensure consistency with the new constitution.