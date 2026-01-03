# Quickstart Guide: Integrated RAG Chatbot for Published Book

## Overview
This guide will help you quickly set up and run the Integrated RAG Chatbot for Published Book. The system allows users to ask questions about book content and receive answers grounded in the actual book text.

## Prerequisites
- Python 3.11+
- Access to Cohere API (API key)
- Access to Qdrant Cloud (URL and API key)
- Access to Neon Serverless Postgres (connection string)

## Environment Setup
1. Create a `.env` file in the project root with the following variables:
   ```bash
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_CLUSTER_ID=your_qdrant_cluster_id
   NEON_DATABASE_URL=your_neon_database_url
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Service
1. Start the FastAPI server:
   ```bash
   uvicorn src.api.main:app --reload --port 8000
   ```

2. Verify the service is running:
   - Navigate to `http://localhost:8000/health` to check the health status
   - You should receive a response confirming all dependencies are connected

## Basic Usage
1. **Ingest a book**:
   ```bash
   curl -X POST "http://localhost:8000/ingest/book" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/your/book.pdf" \
     -F "metadata={\"title\":\"Book Title\", \"author\":\"Author Name\"}"
   ```

2. **Ask a question**:
   ```bash
   curl -X POST "http://localhost:8000/chat/query" \
     -H "Content-Type: application/json" \
     -d '{
       "book_id": "your-book-id",
       "query": "What is the main theme of this book?"
     }'
   ```

3. **Ask about selected text**:
   ```bash
   curl -X POST "http://localhost:8000/chat/query-selected-text" \
     -H "Content-Type: application/json" \
     -d '{
       "book_id": "your-book-id",
       "query": "What does this passage mean?",
       "selected_text": "The specific text selected by the user..."
     }'
   ```

## Important Notes
- All responses are grounded in the book content with proper citations
- If the system cannot find relevant information, it will respond with: "The provided book content does not contain sufficient information to answer this question."
- For selected-text queries, retrieval is strictly limited to the provided text
- The system operates within Qdrant Cloud Free Tier and Neon Serverless limits
- No external knowledge or web search is used in generating responses

## Troubleshooting
- If ingestion fails, verify the file format is PDF, EPUB, or Text
- If queries return fallback responses consistently, check that the book was properly ingested
- For performance issues, ensure your environment variables are correctly configured