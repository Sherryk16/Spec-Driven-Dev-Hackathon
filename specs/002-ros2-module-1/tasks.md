# Tasks: AI-Native Book & RAG Chatbot

**Input**: Design documents from `/specs/002-ros2-module-1/`
**Prerequisites**: plan.md, spec.md

## Format: `[ID] [P?] Description`

- **[P]**: Can run in parallel with other [P] tasks.
- Paths are relative to the repository root.

---

## Phase 1: Project Foundation Setup

**Purpose**: Create the basic monorepo structure for the frontend and backend.

- [ ] T001 [P] Create the directory structure for the frontend application in `frontend/`.
- [ ] T002 [P] Create the directory structure for the backend application in `backend/`.
- [ ] T003 [P] Initialize a `package.json` for the `frontend` application (`npm init -y`).
- [ ] T004 [P] Initialize a Python project for the `backend` (e.g., create `pyproject.toml` and `requirements.txt`).
- [ ] T005 [P] Configure top-level linting and formatting tools (e.g., Prettier, EditorConfig).

---

## Phase 2: Docusaurus Site (MVP)

**Purpose**: Build the static Docusaurus site to host the book content. This delivers the core value to all user stories.

**Independent Test**: The Docusaurus site builds successfully and serves the book content locally.

- [ ] T006 Install Docusaurus and its dependencies in `frontend/`.
- [ ] T007 Configure `frontend/docusaurus.config.js` with the book's title, navigation, and module structure.
- [ ] T008 Create placeholder Markdown files for all book modules and chapters under `frontend/docs/`.
- [ ] T009 Write the content for Chapter 1 (ROS 2 Basics) in `frontend/docs/module1/chapter1.md`.
- [ ] T010 Write the content for Chapter 2 (Services, Actions) in `frontend/docs/module1/chapter2.md`.
- [ ] T011 Write the content for Chapter 3 (Python Agents + URDF) in `frontend/docs/module1/chapter3.md`.

**Checkpoint**: MVP is complete. The book is readable on a local Docusaurus site.

---

## Phase 3: RAG Backend (FastAPI)

**Purpose**: Develop the backend API to power the RAG chatbot.

**Independent Test**: The FastAPI server runs, and API endpoints can be successfully called via an API client like Postman or Insomnia.

- [ ] T012 [P] Add FastAPI and other Python dependencies (e.g., `uvicorn`, `pydantic`, `qdrant-client`, `openai`, `psycopg2-binary`) to `backend/requirements.txt`.
- [ ] T013 Set up the basic FastAPI application object in `backend/src/main.py`.
- [ ] T014 Implement the Postgres database connection and session management in `backend/src/core/database.py`.
- [ ] T015 Implement the Pydantic models for the API request/response based on `contracts/openapi.yaml` in `backend/src/core/schemas.py`.
- [ ] T016 Implement the chat session and message history database logic based on `data-model.md` in `backend/src/services/history_service.py`.
- [ ] T017 Implement the Qdrant client and vector search logic in `backend/src/services/rag_service.py`.
- [ ] T018 Implement the main chat endpoint logic in `backend/src/api/chat.py`, tying together the history and RAG services.
- [ ] T019 Implement the content embedding script in `backend/src/scripts/embed_content.py`.

**Checkpoint**: Backend is complete and can respond to API requests.

---

## Phase 4: Frontend Chatbot Integration

**Purpose**: Connect the Docusaurus frontend to the FastAPI backend.

**Independent Test**: The chatbot UI appears on the Docusaurus site and can successfully send/receive messages to/from the local backend.

- [ ] T020 Create a custom Docusaurus plugin for the chatbot in `frontend/src/plugins/chatbot/`.
- [ ] T021 Implement the React component for the chatbot UI in `frontend/src/plugins/chatbot/ChatbotWidget.js`.
- [ ] T022 Add state management to the React component for handling messages and API calls.
- [ ] T023 Connect the chatbot UI to the FastAPI `/chat` endpoint.
- [ ] T024 Style the chatbot component to be a non-intrusive floating widget.

**Checkpoint**: The full application is functional on a local machine.

---

## Phase 5: Polish & Deployment

**Purpose**: Final documentation, cleanup, and deployment preparation.

- [ ] T025 [P] Write a comprehensive `README.md` for the `backend/` directory.
- [ ] T026 [P] Write a comprehensive `README.md` for the `frontend/` directory.
- [ ] T027 [P] Create a `render.yaml` file to configure the deployment of the FastAPI backend on Render.
- [ ] T028 [P] Add deployment instructions for the Docusaurus site.
- [ ] T029 Validate the full workflow described in `quickstart.md`.

---

## Dependencies & Execution Order

- **Phase 1 (Foundation)** must be completed first.
- **Phase 2 (Docusaurus Site)** can proceed after Phase 1. This delivers the MVP.
- **Phase 3 (RAG Backend)** can run in parallel with Phase 2.
- **Phase 4 (Integration)** depends on the completion of both Phase 2 and Phase 3.
- **Phase 5 (Polish)** depends on the completion of all prior phases.
