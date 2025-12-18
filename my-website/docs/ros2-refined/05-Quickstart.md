---
sidebar_position: 5
---

# Quickstart

This guide provides the basic steps to set up and run the AI-Native Book and RAG Chatbot project locally. 

## Prerequisites

- Python 3.9+ and `pip`
- Node.js 18+ and `npm` or `yarn`
- Docker and Docker Compose
- Access keys for OpenAI

## Backend Setup (FastAPI)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    - Create a `.env` file in the `backend` directory.
    - Add the following variables:
      ```
      OPENAI_API_KEY="your_openai_key"
      DATABASE_URL="your_neon_postgres_connection_string"
      QDRANT_URL="your_qdrant_cloud_url"
      QDRANT_API_KEY="your_qdrant_api_key"
      ```

5.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## Frontend Setup (Docusaurus)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the Docusaurus development server:**
    ```bash
    npm run start
    ```
    The book will be available at `http://localhost:3000`. The chatbot UI will be embedded in the site.   

## Content Embedding

To populate the Qdrant vector database with the book's content, you will need to run the embedding script.

1.  **Ensure the backend server is NOT running.**
2.  **Run the embedding script from the `backend` directory:**
    ```bash
    python -m scripts.embed_content
    ```
    This script will parse the Markdown files from the `frontend/docs` directory, chunk them, generate emb
eddings using the OpenAI API, and upload them to Qdrant.
