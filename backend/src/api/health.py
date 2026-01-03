"""
Health check endpoint for the Integrated RAG Chatbot.
Verifies the status of all dependencies.
"""
from fastapi import APIRouter
from datetime import datetime
from src.models.api_models import HealthStatus
from src.services.cohere_service import cohere_client
from src.vector_store.qdrant_service import qdrant_service
from src.config.settings import settings


router = APIRouter()


@router.get("/", response_model=HealthStatus)
async def health_check():
    """
    Check the health status of the service and its dependencies.
    """
    dependencies = {
        "cohere_api": "disconnected",
        "qdrant": "disconnected",
        "neon_postgres": "not_implemented"  # We don't have DB connection implemented yet
    }
    
    # Check Cohere API
    try:
        # Make a simple call to Cohere to verify the connection
        response = cohere_client.client.generate(
            model="command-r-plus",
            prompt="Say 'connected' in one word.",
            max_tokens=5
        )
        if response and response.generations:
            dependencies["cohere_api"] = "connected"
    except Exception:
        dependencies["cohere_api"] = "disconnected"
    
    # Check Qdrant
    try:
        # Try to get collection info to verify connection
        qdrant_service.client.get_collection(qdrant_service.collection_name)
        dependencies["qdrant"] = "connected"
    except Exception:
        dependencies["qdrant"] = "disconnected"
    
    # Determine overall status
    all_connected = all(status == "connected" for status in dependencies.values())
    status = "healthy" if all_connected else "unhealthy"
    
    health_status = HealthStatus(
        status=status,
        timestamp=datetime.utcnow(),
        dependencies=dependencies
    )
    
    return health_status