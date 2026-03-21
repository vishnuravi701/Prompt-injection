"""
Application configuration settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # API Configuration
    API_TITLE = "Prompt Injection Prevention API"
    API_VERSION = "1.0.0"
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = "gemini-pro"
    
    # Model Paths
    MODEL_PATH = os.getenv("MODEL_PATH", "./models/trained_model/model.pkl")
    PREPROCESSOR_PATH = os.getenv("PREPROCESSOR_PATH", "./models/preprocessing/preprocessor.pkl")
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Frontend
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 3000))
    FRONTEND_URL = os.getenv("REACT_APP_API_URL", "http://localhost:3000")

settings = Settings()
