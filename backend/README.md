# Integrated RAG Chatbot for Published Book

This project implements a Retrieval-Augmented Generation (RAG) chatbot that answers questions strictly from book content, including support for queries restricted to user-selected text only. The system uses Cohere API for embeddings and generation, FastAPI for backend services, Qdrant Cloud for vector storage, and Neon Serverless Postgres for metadata.

## Architecture

The system follows a clean separation of concerns with the following layers:

- **Ingestion Layer**: Handles book file processing, text extraction, and chunking
- **Embedding Layer**: Generates vector embeddings using Cohere API
- **Storage Layer**: Stores vectors in Qdrant Cloud and metadata in Neon Postgres
- **Retrieval Layer**: Performs vector similarity search to find relevant content
- **Generation Layer**: Creates responses based on retrieved content using Cohere
- **API Layer**: Provides RESTful endpoints for interaction

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file (see `.env.example`)
4. Run the application: `uvicorn src.api.main:app --reload --port 8000`

## Environment Variables

The application requires the following environment variables:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: URL for your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for Qdrant Cloud
- `QDRANT_CLUSTER_ID`: Cluster ID for Qdrant Cloud
- `NEON_DATABASE_URL`: Connection string for Neon Serverless Postgres

## API Endpoints

- `POST /ingest/book`: Ingest a book file (PDF, EPUB, or Text)
- `POST /chat/query`: Query book content
- `POST /chat/query-selected-text`: Query user-selected text only
- `GET /health`: Check system health

## Features

1. **Faithful Responses**: All answers are grounded in the actual book content
2. **Citation Tracking**: Every answer includes citations to specific book passages
3. **Selected Text Queries**: Ability to limit queries to user-selected text only
4. **No Hallucinations**: System will respond with a fallback message if content is insufficient
5. **Free Tier Compatible**: Designed to operate within Qdrant Cloud and Neon Serverless limits

## Implementation Details

- Text is chunked deterministically with overlap to preserve context
- Vector embeddings are generated using Cohere's multilingual model
- Retrieved chunks are reranked for relevance before generation
- Responses are validated to ensure they're grounded in provided context
- Structured logging for monitoring and debugging