from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from typing import Optional

app = FastAPI(title="Customer Interaction Platform Gateway")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs
CHAT_SERVICE_URL = os.getenv("CHAT_SERVICE_URL", "http://chat-service:8000")
SENTIMENT_SERVICE_URL = os.getenv("SENTIMENT_SERVICE_URL", "http://sentiment-service:8000")

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class SentimentRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {
        "service": "API Gateway",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "sentiment": "/sentiment",
            "health": "/health"
        }
    }

@app.post("/chat")
async def chat(req: ChatRequest):
    """Forward chat requests to chat service"""
    try:
        response = requests.post(
            f"{CHAT_SERVICE_URL}/chat",
            json=req.model_dump(),
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Chat service unavailable: {str(e)}"
        )

@app.post("/sentiment")
async def analyze_sentiment(req: SentimentRequest):
    """Forward sentiment analysis requests to sentiment service"""
    try:
        response = requests.post(
            f"{SENTIMENT_SERVICE_URL}/analyze",
            json=req.model_dump(),
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Sentiment service unavailable: {str(e)}"
        )

@app.get("/health")
def health():
    """Health check endpoint"""
    services_status = {}
    
    # Check chat service
    try:
        chat_response = requests.get(f"{CHAT_SERVICE_URL}/health", timeout=2)
        services_status["chat-service"] = "healthy" if chat_response.status_code == 200 else "unhealthy"
    except:
        services_status["chat-service"] = "unavailable"
    
    # Check sentiment service
    try:
        sentiment_response = requests.get(f"{SENTIMENT_SERVICE_URL}/health", timeout=2)
        services_status["sentiment-service"] = "healthy" if sentiment_response.status_code == 200 else "unhealthy"
    except:
        services_status["sentiment-service"] = "unavailable"
    
    return {
        "status": "ok",
        "service": "gateway",
        "services": services_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
