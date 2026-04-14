"""
Core Configuration Module
Manages environment variables and application settings
"""
import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    For production deployment (AWS EC2), set these in .env or environment.
    """
    
    # Application
    APP_NAME: str = "PlagLe API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "plagle_db"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".txt", ".pdf", ".docx"]
    
    # Plagiarism Detection
    SIMILARITY_THRESHOLD: float = 0.15  # 15% similarity triggers report
    ALGORITHM_ID: int = 1  # Default algorithm
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        # Add your production frontend URL here
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Call this function to get configuration throughout the app.
    """
    return Settings()
