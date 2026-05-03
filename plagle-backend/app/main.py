"""
PlagLe FastAPI Application - Main Entry Point
Production-ready plagiarism detection backend
"""
# Web framework and standard utilities
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Standard logging and time tracking
import logging
import time

from app.core.config import get_settings
from app.core.database import init_db_pool, close_db_pool
from app.core.logging_config import setup_logging
from app.api.routes import router
from app.utils.helpers import ensure_directories

# Initialize settings
settings = get_settings()

# Setup logging first
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events for startup and shutdown.
    Handles database connection pool initialization.
    """
    # Startup
    logger.info("=" * 50)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("=" * 50)
    
    # Ensure directories exist
    ensure_directories()
    logger.info("Required directories verified")
    
    # Initialize database pool
    try:
        init_db_pool()
        logger.info("Database connection pool initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    logger.info(f"Server ready at http://{settings.HOST}:{settings.PORT}")
    logger.info("=" * 50)
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    close_db_pool()
    logger.info("Database connections closed")
    logger.info("Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    **PlagLe - Production-Ready Plagiarism Detection API**
    
    A comprehensive backend system for detecting plagiarism in student submissions.
    
    ## Features
    - 📤 **File Upload**: Supports TXT, PDF, DOCX formats
    - 🔍 **Plagiarism Detection**: TF-IDF based similarity analysis
    - 📊 **PDF Reports**: Auto-generated detailed reports
    - 💾 **Database Storage**: MySQL-backed persistent storage
    - 🚀 **Production Ready**: Logging, error handling, CORS enabled
    
    ## Main Endpoint
    Use `/api/v1/check-plagiarism` for complete flow:
    - Upload file
    - Check plagiarism
    - Generate reports
    - Return results in one call
    
    Perfect for React/Vue/Angular frontend integration!
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    debug=settings.DEBUG
)


# ====== Middleware ======

# CORS Middleware (Essential for frontend connectivity)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests with timing information.
    Useful for monitoring and debugging in production.
    """
    start_time = time.time()
    
    # Log request
    logger.info(f"→ {request.method} {request.url.path}")
    
    # Process request
    try:
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            f"← {request.method} {request.url.path} "
            f"[{response.status_code}] {duration:.3f}s"
        )
        
        return response
    
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"✗ {request.method} {request.url.path} "
            f"FAILED after {duration:.3f}s: {str(e)}"
        )
        raise


# ====== Exception Handlers ======

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler.
    Catches all unhandled exceptions and returns proper JSON response.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
            "path": str(request.url)
        }
    )


# ====== Routes ======

# Include API routes
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health",
        "message": "Welcome to PlagLe API! Visit /docs for interactive documentation."
    }


# ====== Run Application ======

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # Auto-reload in development
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
