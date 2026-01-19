from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class ChatRequest(BaseModel):
    message:str
    session_id:str

@app.post("/chat")
def chat(req: ChatRequest):
    rag_ctx = requests.post(
        "http://rag-service/retrieve",
        json={"query": req.message}
    ).json()

    llm_resp = requests.post(
        "http://llm-service/generate",
        json={
            "prompt": req.message,
            "context": rag_ctx["context"]
        }
    ).json()

    return {
        "response": llm_resp["text"],
        "confidence": llm_resp["confidence"]
    }