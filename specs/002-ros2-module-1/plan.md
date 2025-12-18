# Implementation Plan: AI-Native Book & RAG Chatbot

**Branch**: `002-ros2-module-1` | **Date**: 2025-12-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the architecture for an AI-Native Technical Book on robotics, built with Docusaurus. It includes an integrated RAG (Retrieval-Augmented Generation) chatbot to provide an interactive learning experience. The chatbot backend will be a FastAPI application using Qdrant for vector search, Neon Postgres for chat history, and the OpenAI API for embeddings and generation. The entire system is designed for deployment on Render.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11 (backend), TypeScript (frontend)
**Primary Dependencies**: FastAPI (backend), Docusaurus (frontend), Qdrant, Neon, OpenAI SDK
**Storage**: Neon Serverless Postgres (chat history), Qdrant Cloud (vector embeddings)
**Testing**: pytest (backend), Vitest (frontend)
**Target Platform**: Web
**Project Type**: Web Application (frontend/backend monorepo)
**Performance Goals**: Chatbot responses should start streaming in <3 seconds.
**Constraints**: Must operate within the free tiers of Render, Neon, and Qdrant.
**Scale/Scope**: The book will contain 4-5 modules (~25,000 words). The chatbot is for a single user interacting with the book content.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All aspects of this plan have been checked against the `constitution.md` document (v1.1.1).

- **[PASS] Technical Accuracy**: The plan relies on official documentation for all technical content.
- **[PASS] Coherence & Structure**: The planned book structure follows the required learning arc and module requirements.
- **[PASS] RAG Implementation**: The plan adheres to all mandated technologies for the RAG chatbot (Qdrant, Neon, FastAPI, OpenAI).
- **[PASS] Source & Citation**: The workflow accounts for source transparency and citation requirements.

**Result**: The plan is in full compliance with the constitution. No violations are reported.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (frontend + backend)
backend/
├── src/
│   ├── api/          # FastAPI endpoints
│   ├── core/         # Configuration, core services
│   ├── services/     # Business logic (RAG pipeline)
│   └── scripts/      # Standalone scripts (e.g., embedding)
└── tests/

frontend/
├── docs/             # Docusaurus: Book content (Markdown files)
├── src/
│   ├── components/   # Custom React components
│   ├── pages/        # Custom pages
│   └── plugins/      # Custom local Docusaurus plugins (e.g., chatbot)
└── docusaurus.config.js
```

**Structure Decision**: A monorepo with two main packages, `frontend` and `backend`, is selected. This cleanly separates the Docusaurus book and the FastAPI chatbot API, while keeping them in a single repository for simplicity.


