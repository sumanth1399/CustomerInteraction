from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@router.get("/")
def root():
    return FileResponse("FrontEnd/static/index.html")

@router.get("/health")
def health():
    return {"status": "ok", "service": "chat_service"}

@router.post("/chat")
def chat(req: ChatRequest):
    rag_service_url = os.getenv("RAG_SERVICE_URL", "http://localhost:8002")
    llm_service_url = os.getenv("LLM_SERVICE_URL", "http://localhost:8003")
    
    try:
        # Call RAG service
        rag_response = requests.post(
            f"{rag_service_url}/retrieve",
            json={"query": req.message},
            timeout=10
        )
        rag_response.raise_for_status()
        rag_ctx = rag_response.json()
    except requests.exceptions.RequestException as e:
        logger.warning(f"RAG service error: {str(e)}")
        rag_ctx = {"context": ""}

    try:
        # Call LLM service
        llm_response = requests.post(
            f"{llm_service_url}/generate",
            json={
                "prompt": req.message,
                "context": rag_ctx.get("context", "")
            },
            timeout=30
        )
        llm_response.raise_for_status()
        llm_resp = llm_response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"LLM service error: {str(e)}")
        return {
            "response": f"Service temporarily unavailable. Your message: {req.message}",
            "confidence": 0.0,
            "error": "LLM service unavailable"
        }

    return {
        "response": llm_resp.get("text", ""),
        "confidence": llm_resp.get("confidence", 0.0)
    }