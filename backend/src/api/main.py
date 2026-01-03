"""
Main application entry point for the Integrated RAG Chatbot.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.ingest import router as ingest_router
from src.api.chat import router as chat_router
from src.api.health import router as health_router

# Try to initialize real services, fall back to mock if they fail
try:
    # Try to import and use real services
    from src.services.cohere_service import cohere_client
    from src.vector_store.qdrant_service import qdrant_service
    print("Using real Cohere and Qdrant services")
    USING_MOCK_SERVICES = False
except Exception as e:
    print(f"Failed to initialize real services: {e}")
    print("Falling back to mock services for testing...")

    # Import mock services
    from src.services.mock_cohere_service import cohere_client
    from src.vector_store.mock_qdrant_service import qdrant_service
    USING_MOCK_SERVICES = True

# Print service status
print(f"Cohere client model: {cohere_client.embed_model}")
if hasattr(qdrant_service, 'points'):
    print(f"Qdrant service points count: {len(qdrant_service.points)}")

app = FastAPI(
    title="Integrated RAG Chatbot for Published Book",
    description="A RAG system that answers questions based on book content",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",  # Your Docusaurus frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(ingest_router, prefix="/ingest", tags=["ingestion"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(health_router, prefix="/health", tags=["health"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)