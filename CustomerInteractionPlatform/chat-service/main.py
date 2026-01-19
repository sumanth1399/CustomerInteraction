# from fastapi import FastAPI
# from pydantic import BaseModel
# import requests
# import os

# app = FastAPI(title="Chat Service")

# class ChatRequest(BaseModel):
#     message: str
#     session_id: str

# @app.get("/")
# def root():
#     return {"static/index.html"}

# @app.get("/health")
# def health():
#     return {"status": "ok", "service": "chat-service"}

# @app.post("/chat")
# def chat(req: ChatRequest):
#     rag_service_url = os.getenv("RAG_SERVICE_URL", "http://rag-service:8000")
#     llm_service_url = os.getenv("LLM_SERVICE_URL", "http://llm-service:8000")
    
#     try:
#         # Call RAG service
#         rag_response = requests.post(
#             f"{rag_service_url}/retrieve",
#             json={"query": req.message},
#             timeout=10
#         )
#         rag_response.raise_for_status()
#         rag_ctx = rag_response.json()
#     except requests.exceptions.RequestException as e:
#         # If RAG service unavailable, use empty context
#         rag_ctx = {"context": ""}

#     try:
#         # Call LLM service
#         llm_response = requests.post(
#             f"{llm_service_url}/generate",
#             json={
#                 "prompt": req.message,
#                 "context": rag_ctx.get("context", "")
#             },
#             timeout=30
#         )
#         llm_response.raise_for_status()
#         llm_resp = llm_response.json()
#     except requests.exceptions.RequestException as e:
#         # Return a fallback response if LLM service is unavailable
#         return {
#             "response": f"Service temporarily unavailable. Your message: {req.message}",
#             "confidence": 0.0,
#             "error": "LLM service unavailable"
#         }

#     return {
#         "response": llm_resp.get("text", ""),
#         "confidence": llm_resp.get("confidence", 0.0)
#     }

#     # Mount static files
# app.mount("/static", StaticFiles(directory="static"), name="static")


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Chat Service")

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "service": "chat-service"}

@app.post("/chat")
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
        return {
            "response": f"Service temporarily unavailable. Your message: {req.message}",
            "confidence": 0.0,
            "error": "LLM service unavailable"
        }

    return {
        "response": llm_resp.get("text", ""),
        "confidence": llm_resp.get("confidence", 0.0)
    }

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")