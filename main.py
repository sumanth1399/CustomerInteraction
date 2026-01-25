import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Customer Interaction Platform")

# ==================== SERVICE CONFIGURATION ====================
class ServiceRegistry:
    """Centralized service configuration and management"""
    def __init__(self):
        self.services = {
            "rag_service": os.getenv("RAG_SERVICE_URL", "http://localhost:8002"),
            "llm_service": os.getenv("LLM_SERVICE_URL", "http://localhost:8003"),
            "chat_service": os.getenv("CHAT_SERVICE_URL", "http://localhost:8001"),
        }
    
    def get_service_url(self, service_name: str) -> str:
        return self.services.get(service_name, "")
    
    def log_services(self):
        logger.info("=" * 50)
        logger.info("Service Registry Initialized")
        logger.info("=" * 50)
        for service, url in self.services.items():
            logger.info(f"✓ {service}: {url}")
        logger.info("=" * 50)

# Initialize service registry
service_registry = ServiceRegistry()

# ==================== MIDDLEWARE ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== STARTUP & SHUTDOWN ====================
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    service_registry.log_services()
    logger.info("🚀 Customer Interaction Platform started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Customer Interaction Platform shutting down")

# ==================== IMPORT ROUTERS ====================
from CustomerInteractionPlatform.chat_service.main import router as chat_router

# Include routers from each service
app.include_router(chat_router, prefix="/chat", tags=["chat"])

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
#     uvicorn.run(
#         app,
#         host="0.0.0.0",
#         port=int(os.getenv("PORT", 8000)),
#         log_level="info"
#     )