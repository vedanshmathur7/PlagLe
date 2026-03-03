"""
Database Connection Management
Handles MySQL connection pooling and context management
"""
import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager
from typing import Generator
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Connection pool for better performance
connection_pool = None


def init_db_pool():
    """
    Initialize database connection pool.
    Call this on application startup.
    """
    global connection_pool
    
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="plagle_pool",
            pool_size=10,
            pool_reset_session=True,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            autocommit=False
        )
        logger.info("Database connection pool initialized successfully")
    except mysql.connector.Error as err:
        logger.error(f"Failed to initialize database pool: {err}")
        raise


def close_db_pool():
    """
    Close database connection pool.
    Call this on application shutdown.
    """
    global connection_pool
    if connection_pool:
        # Pool doesn't have a direct close method, set to None
        connection_pool = None
        logger.info("Database connection pool closed")


@contextmanager
def get_db_connection() -> Generator:
    """
    Context manager for database connections.
    Automatically handles connection cleanup and error rollback.
    
    Usage:
        with get_db_connection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM User")
    """
    if not connection_pool:
        raise RuntimeError("Database pool not initialized. Call init_db_pool() first.")
    
    connection = None
    try:
        connection = connection_pool.get_connection()
        yield connection
        connection.commit()
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()


def get_db():
    """
    Dependency injection for FastAPI routes.
    Yields a database connection that auto-commits on success.
    """
    with get_db_connection() as db:
        yield db
