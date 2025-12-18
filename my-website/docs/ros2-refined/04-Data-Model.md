---
sidebar_position: 4
---

# Data Model

This document defines the database schema for the RAG chatbot, which will be implemented using Neon Serverless Postgres.

## Schema Overview

The data model consists of two primary tables designed to store chat history: `chat_sessions` and `chat_messages`. This allows for tracking conversations and associating messages with specific user sessions.     

### Table: `chat_sessions`

Stores a record for each unique chat session.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `UUID` | **Primary Key**, `default: gen_random_uuid()` | Unique identifier for the chat session. 
|
| `user_id` | `VARCHAR(255)` | `NOT NULL` | An identifier for the end-user (e.g., a browser session ID or 
a logged-in user ID). |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | `NOT NULL`, `default: now()` | Timestamp when the session wa
s initiated. |

### Table: `chat_messages`

Stores individual messages belonging to a chat session.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGSERIAL` | **Primary Key** | Auto-incrementing unique identifier for the message. |
| `session_id` | `UUID` | `NOT NULL`, **Foreign Key** -> `chat_sessions.id` | Links the message to a speci
fic chat session. |
| `role` | `VARCHAR(50)` | `NOT NULL` | The originator of the message. Must be either 'user' or 'assistant
'. |
| `content` | `TEXT` | `NOT NULL` | The textual content of the message. |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | `NOT NULL`, `default: now()` | Timestamp when the message wa
s recorded. |
| `metadata` | `JSONB` | `NULL` | For 'assistant' messages, this can store structured data like a list of 
source documents used for the response. |

## Relationships

- A `chat_session` can have many `chat_messages`.
- Each `chat_message` belongs to exactly one `chat_session`.

## SQL Definition

```sql
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE TABLE chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    metadata JSONB
);

CREATE INDEX idx_chat_messages_session_id ON chat_messages(session_id);
```
