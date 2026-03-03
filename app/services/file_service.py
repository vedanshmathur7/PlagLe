"""
File Service - Handles file uploads, validation, and storage
"""
import os
import hashlib
import shutil
from datetime import datetime
from typing import Tuple, List
from fastapi import UploadFile, HTTPException
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FileService:
    """Service for handling file operations"""
    
    def __init__(self):
        """Initialize directories"""
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        os.makedirs(settings.REPORT_DIR, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> None:
        """
        Validate file extension and size.
        Raises HTTPException if validation fails.
        """
        # Check extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Check size (read file size)
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset to beginning
        
        if file_size > settings.MAX_FILE_SIZE:
            max_mb = settings.MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {max_mb}MB"
            )
        
        logger.info(f"File validated: {file.filename} ({file_size} bytes)")
    
    def calculate_file_hash(self, file_path: str) -> str:
        """
        Calculate SHA256 hash of a file.
        Used for duplicate detection.
        """
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    async def save_upload(self, file: UploadFile, submission_id: int) -> Tuple[str, str]:
        """
        Save uploaded file to disk.
        Returns (file_path, file_hash).
        """
        # Validate first
        self.validate_file(file)
        
        # Create submission subdirectory
        submission_dir = os.path.join(settings.UPLOAD_DIR, f"submission_{submission_id}")
        os.makedirs(submission_dir, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = os.path.splitext(file.filename)[1]
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(submission_dir, safe_filename)
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File saved: {file_path}")
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
        # Calculate hash
        file_hash = self.calculate_file_hash(file_path)
        
        # Convert to absolute path
        absolute_path = os.path.abspath(file_path)
        
        return absolute_path, file_hash
    
    async def save_multiple_uploads(
        self, 
        files: List[UploadFile], 
        submission_id: int
    ) -> List[Tuple[str, str, str]]:
        """
        Save multiple files.
        Returns list of (filename, file_path, file_hash) tuples.
        """
        results = []
        
        for file in files:
            try:
                file_path, file_hash = await self.save_upload(file, submission_id)
                results.append((file.filename, file_path, file_hash))
            except HTTPException:
                raise  # Re-raise validation errors
            except Exception as e:
                logger.error(f"Error processing {file.filename}: {e}")
                # Continue with other files
                continue
        
        return results
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from disk.
        Returns True if successful.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return False
