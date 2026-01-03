"""
Simplified chatbot for testing purposes.
This version bypasses all external services and uses a simple knowledge base.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
import json

# Simple in-memory knowledge base
KNOWLEDGE_BASE = [
    {
        "id": str(uuid4()),
        "content": "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. It deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing.",
        "metadata": {"chapter": "Introduction to Robotics", "source": "Robotics and AI Handbook"}
    },
    {
        "id": str(uuid4()),
        "content": "Artificial intelligence (AI) in robotics is the combination of sensors, software, and data-processing capabilities that allow robots to learn from experience, adapt to new inputs, and perform human-like tasks. These intelligent machines can interpret stimuli and respond accordingly.",
        "metadata": {"chapter": "AI in Robotics", "source": "Robotics and AI Handbook"}
    },
    {
        "id": str(uuid4()),
        "content": "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.",
        "metadata": {"chapter": "ROS 2 Fundamentals", "source": "Robotics and AI Handbook"}
    },
    {
        "id": str(uuid4()),
        "content": "A digital twin is a virtual representation that serves as the real-time digital counterpart of a physical object or process. In robotics, digital twins enable engineers to simulate, predict, and optimize robot behavior before implementing changes in the physical world.",
        "metadata": {"chapter": "Digital Twins in Robotics", "source": "Robotics and AI Handbook"}
    }
]

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class Citation(BaseModel):
    chunk_id: Optional[str]
    chapter: Optional[str]
    section: Optional[str]
    page_number: Optional[int]

class QueryResponse(BaseModel):
    response_id: str
    answer: str
    citations: List[Citation]
    query_time: float

app = FastAPI(
    title="Simplified RAG Chatbot",
    description="A simplified chatbot that works without external dependencies",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def simple_search(query: str, knowledge_base: List[dict]) -> List[dict]:
    """Simple search function that matches keywords in the knowledge base."""
    query_lower = query.lower()
    results = []
    
    for item in knowledge_base:
        content_lower = item["content"].lower()
        if any(word in content_lower for word in query_lower.split()):
            # Simple scoring based on keyword matches
            score = sum(1 for word in query_lower.split() if word in content_lower)
            results.append({
                "content": item["content"],
                "metadata": item["metadata"],
                "similarity_score": score,
                "chunk_id": item["id"]
            })
    
    # Sort by similarity score
    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return results[:3]  # Return top 3 results

@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(request: ChatRequest):
    """Simplified chat endpoint that uses the knowledge base."""
    import time
    start_time = time.time()
    
    # Search the knowledge base for relevant information
    search_results = simple_search(request.query, KNOWLEDGE_BASE)
    
    if search_results:
        # Build response from found information
        response_parts = ["Based on the robotics and AI handbook:"]
        citations = []
        
        for result in search_results:
            response_parts.append(result["content"])
            citations.append(Citation(
                chunk_id=result.get("chunk_id"),
                chapter=result["metadata"].get("chapter"),
                section=result["metadata"].get("section"),
                page_number=result["metadata"].get("page_number")
            ))
        
        answer = " ".join(response_parts)
    else:
        # If no relevant information found, provide a general response
        answer = (
            "I'm a simplified chatbot based on a robotics and AI handbook. "
            "I can answer questions about robotics, AI, ROS 2, digital twins, and related topics. "
            "Try asking about specific topics like 'What is robotics?' or 'Explain ROS 2'."
        )
        citations = []
    
    response = QueryResponse(
        response_id=str(uuid4()),
        answer=answer,
        citations=citations,
        query_time=time.time() - start_time
    )
    
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2025-12-19T17:25:34.121136",
        "dependencies": {
            "knowledge_base": "connected",
            "search_engine": "operational"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)