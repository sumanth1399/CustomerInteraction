from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from main import router

app = FastAPI(title="Chat Service")

# Mount static files
app.mount("/static", StaticFiles(directory="FrontEnd/static"), name="static")

# Include router
app.include_router(router)