from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from main import router

app = FastAPI(title="Chat Service")

# Mount static files
app.mount("/static", StaticFiles(directory="FrontEnd/static"), name="static")

# Include router
app.include_router(router)


# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from .main import router
# import os
# from pathlib import Path

# app = FastAPI(title="Chat Service")

# # Get the current directory of this file
# current_dir = Path(__file__).parent

# # Mount static files
# app.mount("/static", StaticFiles(directory=str(current_dir / "FrontEnd" / "static")), name="static")

# # Include router
# app.include_router(router)