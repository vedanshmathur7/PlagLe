"""
Pydantic Schemas for Request/Response Validation
Defines data models for API endpoints
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ====== Enums ======

class UserRole(str, Enum):
    """User role enumeration"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class RiskLevel(str, Enum):
    """Plagiarism risk classification"""
    LOW = "Low Risk"
    MEDIUM = "Medium Risk"
    HIGH = "High Risk"


# ====== User Schemas ======

class UserBase(BaseModel):
    """Base user information"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    """User response schema"""
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ====== File Upload Schemas ======

class FileUploadResponse(BaseModel):
    """Response after file upload"""
    document_id: int
    file_name: str
    file_path: str
    file_hash: str
    uploaded_at: datetime


# ====== Plagiarism Check Schemas ======

class PlagiarismCheckRequest(BaseModel):
    """Request to check plagiarism between documents"""
    assignment_id: int = Field(..., description="Assignment ID for context")
    student_id: int = Field(..., description="Student who submitted")
    algorithm_id: int = Field(default=1, description="Algorithm to use for comparison")


class SimilarityResult(BaseModel):
    """Single similarity comparison result"""
    similarity_id: int
    doc1_id: int
    doc1_name: str
    student1_name: str
    doc2_id: int
    doc2_name: str
    student2_name: str
    score: float = Field(..., description="Similarity score (0.0 - 1.0)")
    score_percentage: float = Field(..., description="Score as percentage")
    risk_level: str
    compared_at: datetime


class PlagiarismCheckResponse(BaseModel):
    """Response from plagiarism check"""
    document_id: int
    file_name: str
    total_comparisons: int
    similarities_found: int
    threshold: float
    results: List[SimilarityResult]
    message: str


# ====== Report Schemas ======

class ReportGenerationRequest(BaseModel):
    """Request to generate a PDF report"""
    similarity_id: int
    generated_by: int = Field(..., description="User ID of report generator")


class ReportResponse(BaseModel):
    """Response after report generation"""
    report_id: int
    similarity_id: int
    report_url: str
    report_pdf_path: str
    summary_notes: str
    created_at: datetime


# ====== Batch Upload Schema ======

class BatchUploadResponse(BaseModel):
    """Response from batch file upload"""
    success_count: int
    failed_count: int
    uploaded_files: List[FileUploadResponse]
    errors: List[str]


class DirectCompareResponse(BaseModel):
    """Response for on-the-fly direct document comparison"""
    file1_name: str
    file2_name: str
    student1_id: int
    student2_id: int
    assignment_id: int
    score: float = Field(..., description="Similarity score (0.0 - 1.0)")
    score_percentage: float = Field(..., description="Score as percentage")
    risk_level: str
    message: str

# ====== Complete Flow Response ======

class CompleteCheckResponse(BaseModel):
    """
    Complete response for upload + check + report flow.
    This is the primary response for frontend integration.
    """
    success: bool
    message: str
    document: FileUploadResponse
    plagiarism_check: Optional[PlagiarismCheckResponse] = None
    reports: List[ReportResponse] = []
    

# ====== Error Response ======

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# ====== Health Check ======

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str
    database: str
