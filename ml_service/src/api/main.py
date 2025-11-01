from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from loguru import logger

from .routes import router

# Configure logging
logger.add("logs/ml_service.log", rotation="10 MB", retention="10 days")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting ML Service...")
    
    # Load models (you can add model loading here)
    # from src.pipelines.rag_pipeline import load_models
    # await load_models()
    
    yield
    
    # Shutdown
    logger.info("Shutting down ML Service...")


app = FastAPI(
    title="Health AI Platform - ML Service",
    description="ML pipelines for retrieval, summarization, and verification",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Health AI Platform ML Service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}

