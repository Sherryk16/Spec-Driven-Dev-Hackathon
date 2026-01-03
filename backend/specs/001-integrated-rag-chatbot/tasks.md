---

description: "Task list for Integrated RAG Chatbot for Published Book"
---

# Tasks: Integrated RAG Chatbot for Published Book

**Input**: Design documents from `/specs/001-integrated-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with FastAPI framework
- [X] T002 Initialize Python project with Cohere, Qdrant, Neon Postgres dependencies
- [X] T003 [P] Configure linting and formatting tools ensuring no OpenAI dependencies
- [X] T004 Create requirements.txt with all required dependencies
- [X] T005 [P] Set up configuration management with environment variables only

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Setup Neon Serverless Postgres database schema and migrations framework
- [X] T007 [P] Configure Cohere API integration (no OpenAI dependencies)
- [X] T008 [P] Setup Qdrant Cloud vector storage integration
- [X] T009 Create base models/entities that all stories depend on
- [X] T010 Configure error handling and logging infrastructure for RAG system
- [X] T011 Setup environment configuration management with Cohere API keys
- [X] T012 [P] Implement ingestion layer with text chunking (deterministic, with overlap and metadata)
- [X] T013 [P] Implement retrieval layer with proper citation capabilities
- [X] T014 [P] Implement generation layer ensuring grounded responses only
- [X] T015 Create configuration settings for Qdrant, Neon, and Cohere
- [X] T016 Implement health check dependencies verification

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Query Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable readers to ask questions about book content and receive accurate answers with citations

**Independent Test**: Can be fully tested by submitting a question about the book content and verifying that the response is grounded in the actual book text with proper citations.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T017 [P] [US1] Contract test for POST /chat/query in tests/contract/test_chat.py
- [ ] T018 [P] [US1] Integration test for book query user journey in tests/integration/test_chat.py

### Implementation for User Story 1

- [X] T019 [P] [US1] Create BookContent model in src/models/book_content.py
- [X] T020 [P] [US1] Create UserQuery model in src/models/user_query.py
- [X] T021 [P] [US1] Create RetrievedChunk model in src/models/retrieved_chunk.py
- [X] T022 [P] [US1] Create GeneratedResponse model in src/models/generated_response.py
- [X] T023 [US1] Implement ingestion service in src/services/ingestion_service.py (depends on T019)
- [X] T024 [US1] Implement retrieval service in src/services/retrieval_service.py (depends on T019, T021)
- [X] T025 [US1] Implement generation service in src/services/generation_service.py (depends on T020, T021, T022)
- [X] T026 [US1] Implement chat endpoint in src/api/chat.py with proper citation capabilities
- [X] T027 [US1] Add validation and error handling for grounded generation
- [X] T028 [US1] Add logging for user story 1 operations with citation tracking
- [X] T029 [US1] Implement fallback response logic: "The provided book content does not contain sufficient information to answer this question."

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Query Selected Text (Priority: P2)

**Goal**: Allow readers to ask questions limited to user-selected text with answers restricted to that text only

**Independent Test**: Can be fully tested by selecting specific text in a book, asking a question about that text, and verifying that the response is limited to information from the selected text only.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US2] Contract test for POST /chat/query-selected-text in tests/contract/test_chat.py
- [ ] T031 [P] [US2] Integration test for selected text query user journey in tests/integration/test_chat.py

### Implementation for User Story 2

- [X] T032 [P] [US2] Create UserSelection model in src/models/user_selection.py
- [X] T033 [US2] Enhance retrieval service in src/services/retrieval_service.py to support user-selected text (depends on T032)
- [X] T034 [US2] Implement selected text isolation in src/services/retrieval_service.py
- [X] T035 [US2] Implement selected text query endpoint in src/api/chat.py
- [X] T036 [US2] Integrate with User Story 1 components for limited retrieval (if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Ingest New Book Content (Priority: P3)

**Goal**: Enable developers to ingest new book content so the RAG system can answer questions about that book

**Independent Test**: Can be fully tested by uploading a book file and verifying that it's properly processed, chunked, and indexed in the vector database.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US3] Contract test for POST /ingest/book in tests/contract/test_ingest.py
- [ ] T038 [P] [US3] Integration test for book ingestion user journey in tests/integration/test_ingest.py

### Implementation for User Story 3

- [X] T039 [P] [US3] Create BookMetadata model in src/models/book_metadata.py
- [X] T040 [US3] Implement book management service in src/services/book_management_service.py
- [X] T041 [US3] Implement book ingestion endpoint in src/api/ingest.py
- [X] T042 [US3] Implement file format validation for PDF, EPUB, Text
- [X] T043 [US3] Implement text extraction for PDF, EPUB, Text formats
- [X] T044 [US3] Integrate with ingestion service from US1 (T023)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T045 [P] Documentation updates in docs/ (including API documentation, RAG behavior explanation)
- [ ] T046 Code cleanup and refactoring to ensure modularity between ingestion/retrieval/generation
- [ ] T047 Performance optimization for large books and multiple concurrent users
- [ ] T048 [P] Additional unit tests (if requested) in tests/unit/ for each RAG component
- [ ] T049 Security hardening to prevent unauthorized content access
- [ ] T050 Run quickstart.md validation with Cohere API and Qdrant Cloud
- [ ] T051 Validate that all responses include proper citations to book passages
- [ ] T052 Verify no hallucinations occur and fallback responses work correctly
- [ ] T053 Test user-selected text retrieval functionality
- [ ] T054 Implement structured logging for all RAG pipeline steps
- [ ] T055 Add comprehensive error handling and graceful degradation
- [ ] T056 Final validation against all success criteria from spec

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for POST /chat/query in tests/contract/test_chat.py"
Task: "Integration test for book query user journey in tests/integration/test_chat.py"

# Launch all models for User Story 1 together:
Task: "Create BookContent model in src/models/book_content.py"
Task: "Create UserQuery model in src/models/user_query.py"
Task: "Create RetrievedChunk model in src/models/retrieved_chunk.py"
Task: "Create GeneratedResponse model in src/models/generated_response.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence