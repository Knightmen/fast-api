from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables as early as possible so that they are available
# to any modules (e.g., routers) imported later in this file.
# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Import routers AFTER loading environment variables to ensure they can access them
from .routers import user, resume, session
from .langsmith_config import get_langsmith_status, setup_langsmith_tracing

# Initialize LangSmith tracing
setup_langsmith_tracing()

app = FastAPI(
    title="FastAPI Backend",
    description="A FastAPI-based backend application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(resume.router)
app.include_router(session.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Backend",
        "status": "running",
        "monitoring": "LangSmith enabled"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    } 

@app.get("/langsmith/status")
async def langsmith_status():
    """Get LangSmith monitoring configuration and status."""
    return {
        "langsmith": get_langsmith_status(),
        "message": "LangSmith monitoring status"
    } 

