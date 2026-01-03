# RAG Chatbot Setup Instructions

This document provides instructions to set up and run the RAG (Retrieval-Augmented Generation) chatbot properly.

## Prerequisites

1. Python 3.11+ installed
2. Node.js and npm installed (for the frontend)
3. Backend dependencies installed
4. Environment variables configured (see backend/.env.example)

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file with the following variables:
   ```
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   QDRANT_CLUSTER_ID=your_qdrant_cluster_id
   NEON_DATABASE_URL=your_neon_database_url
   ```

4. Start the backend server:
   ```bash
   python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000
   ```

## Ingesting Sample Book Content

For the chatbot to work properly, you need to ingest book content first. We've provided a sample book with robotics and AI content:

1. Make sure your backend server is running on port 8000
2. In a new terminal window, navigate to the backend directory and run the ingestion script:
   ```bash
   cd backend
   python ingest_book.py
   ```

This will upload the sample book with robotics and AI content to the system. After ingestion, the chatbot will be able to answer questions about:
- Robotics fundamentals
- AI in robotics
- ROS 2 concepts
- Digital twins
- NVIDIA Isaac platform
- Vision-Language-Action systems

## Frontend Setup

1. Navigate to the my-website directory:
   ```bash
   cd my-website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run start
   ```

## Troubleshooting

1. If the chatbot responds with "No book content is currently available in the system":
   - Make sure you've ingested a book using the ingestion script
   - Verify that your backend server is running and connected to Qdrant and your database

2. If you see "Could not connect to the chatbot":
   - Verify that the backend server is running on port 8000
   - Check that your firewall isn't blocking the connection

3. If you get errors during ingestion:
   - Ensure all environment variables are properly set
   - Check that your Qdrant and database connections are working