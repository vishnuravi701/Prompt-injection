"""
Main FastAPI application for Prompt Injection Prevention & Education Website
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import logging

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Configure logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Prompt Injection Prevention API",
    description="API for detecting and analyzing prompt injection attempts",
    version="1.0.0"
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:3001").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes (to be created)
# from api.routes import analysis_routes, gemini_routes

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Prompt Injection Prevention API",
        "version": "1.0.0"
    }

# Include API routes
from backend.api.routes import router
app.include_router(router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Prompt Injection Prevention & Education API",
        "docs": "/docs",
        "version": "1.0.0"
    }

from backend.api.routes import router

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    
    logger.info(f"Starting backend server at {host}:{port}")
    uvicorn.run(app, host=host, port=port)
