"""
Logging Configuration
Sets up structured logging for production use
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.config import get_settings

settings = get_settings()


def setup_logging():
    """
    Configure application-wide logging.
    Logs to both console and rotating file.
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(settings.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Root logger configuration
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)
    
    # File handler with rotation (10MB per file, keep 5 backups)
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("mysql.connector").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully")
