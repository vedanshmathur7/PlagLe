"""
API Routes - FastAPI endpoint definitions
Production-ready with proper error handling and documentation
"""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from typing import List, Optional
import logging
from datetime import datetime
import mysql.connector

from app.core.database import get_db
from app.core.config import get_settings
from app.models.schemas import (
    CompleteCheckResponse,
    PlagiarismCheckResponse,
    ReportResponse,
    SimilarityResult,
    FileUploadResponse,
    ErrorResponse,
    HealthResponse,
    DirectCompareResponse
)
from app.services.file_service import FileService
from app.services.plagiarism_service import PlagiarismService
from app.services.report_service import ReportService

# Import extraction logic for direct compare
from app.utils.similarity_engine import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_docx,
    preprocess_text,
    calculate_similarity
)

# Import classify_risk from report_generator for risk level calculation
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from app.utils.report_generator import classify_risk

logger = logging.getLogger(__name__)
settings = get_settings()

# Create API router
router = APIRouter(prefix="/api/v1", tags=["PlagLe API"])


# ====== Health Check ======

@router.get("/health", response_model=HealthResponse)
async def health_check(db=Depends(get_db)):
    """
    Health check endpoint.
    Verifies API and database connectivity.
    """
    try:
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        timestamp=datetime.now(),
        version=settings.APP_VERSION,
        database=db_status
    )


# ====== Complete Flow: Upload + Check + Report ======

@router.post("/check-plagiarism", response_model=CompleteCheckResponse)
async def check_plagiarism_complete(
    file: UploadFile = File(...),
    assignment_id: int = Form(...),
    student_id: int = Form(...),
    generated_by: int = Form(...),
    algorithm_id: int = Form(1),
    db=Depends(get_db)
):
    """
    **Complete Plagiarism Check Flow** (Primary Endpoint for Frontend)
    
    Steps:
    1. Upload file
    2. Create submission and document records
    3. Check plagiarism against all documents in same assignment
    4. Generate PDF reports for matches above threshold
    5. Return complete results with report URLs
    
    Perfect for React frontend integration!
    """
    try:
        logger.info(f"Starting plagiarism check for student {student_id}, assignment {assignment_id}")
        
        # Step 1 & 2: Create submission and upload file
        cursor = db.cursor(dictionary=True)
        
        # Validate that the assignment exists
        cursor.execute("SELECT 1 FROM Assignment WHERE assignment_id = %s", (assignment_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Assignment {assignment_id} not found")
            
        # Validate that the student exists
        cursor.execute("SELECT 1 FROM User WHERE user_id = %s AND role = 'student'", (student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        # Create submission
        cursor.execute(
            "INSERT INTO Submission (assignment_id, student_id) VALUES (%s, %s)",
            (assignment_id, student_id)
        )
        db.commit()
        submission_id = cursor.lastrowid
        
        # Upload file
        file_service = FileService()
        file_path, file_hash = await file_service.save_upload(file, submission_id)
        
        # Create document record
        cursor.execute(
            """INSERT INTO Document (submission_id, file_name, file_path, file_hash) 
               VALUES (%s, %s, %s, %s)""",
            (submission_id, file.filename, file_path, file_hash)
        )
        db.commit()
        document_id = cursor.lastrowid
        
        # Get document info for response
        cursor.execute("SELECT * FROM Document WHERE document_id = %s", (document_id,))
        doc_record = cursor.fetchone()
        
        document_response = FileUploadResponse(
            document_id=doc_record['document_id'],
            file_name=doc_record['file_name'],
            file_path=doc_record['file_path'],
            file_hash=doc_record['file_hash'],
            uploaded_at=doc_record['uploaded_at']
        )
        
        # Step 3: Check plagiarism
        plag_service = PlagiarismService(db)
        similarity_results = plag_service.check_plagiarism_for_document(
            document_id, 
            algorithm_id
        )
        
        # Step 4: Generate reports for each similarity above threshold
        report_service = ReportService(db)
        reports = []
        similarity_responses = []
        
        for sim in similarity_results:
            # Generate report
            report_data = report_service.generate_report(
                sim['similarity_id'],
                generated_by
            )
            
            reports.append(ReportResponse(
                report_id=report_data['report_id'],
                similarity_id=sim['similarity_id'],
                report_url=report_data['report_url'],
                report_pdf_path=report_data['report_pdf_path'],
                summary_notes=report_data['summary_notes'],
                created_at=datetime.now()
            ))
            
            # Get student names for response
            comp_doc = sim['compared_doc']
            cursor.execute(
                "SELECT u.first_name, u.last_name FROM User u WHERE u.user_id = %s",
                (comp_doc['student_id'],)
            )
            comp_student = cursor.fetchone()
            
            cursor.execute(
                "SELECT u.first_name, u.last_name FROM User u WHERE u.user_id = %s",
                (student_id,)
            )
            curr_student = cursor.fetchone()
            
            similarity_responses.append(SimilarityResult(
                similarity_id=sim['similarity_id'],
                doc1_id=document_id,
                doc1_name=file.filename,
                student1_name=f"{curr_student['first_name']} {curr_student['last_name']}",
                doc2_id=comp_doc['document_id'],
                doc2_name=comp_doc['file_name'],
                student2_name=f"{comp_student['first_name']} {comp_student['last_name']}",
                score=sim['score'],
                score_percentage=sim['score'] * 100,
                risk_level=report_data['risk_level'],
                compared_at=datetime.now()
            ))
        
        # Build plagiarism check response
        plagiarism_response = PlagiarismCheckResponse(
            document_id=document_id,
            file_name=file.filename,
            total_comparisons=len(plag_service.get_comparison_documents(assignment_id, document_id)),
            similarities_found=len(similarity_results),
            threshold=settings.SIMILARITY_THRESHOLD,
            results=similarity_responses,
            message=f"Found {len(similarity_results)} potential plagiarism matches" if similarity_results else "No plagiarism detected"
        )
        
        # Step 5: Return complete response
        return CompleteCheckResponse(
            success=True,
            message="Plagiarism check completed successfully",
            document=document_response,
            plagiarism_check=plagiarism_response,
            reports=reports
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except mysql.connector.Error as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error in plagiarism check: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ====== Direct Compare (On-the-fly) ======

@router.post("/compare-two-files", response_model=DirectCompareResponse)
async def compare_two_files_directly(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    assignment_id: int = Form(...),
    student_id_1: int = Form(...),
    student_id_2: int = Form(...),
):
    """
    Directly compare two files on-the-fly without saving to the database.
    Useful for quick comparisons or avoiding DB storage for everything.
    """
    try:
        # Helper to extract based on extension
        async def extract_text(file: UploadFile) -> str:
            content = await file.read()
            filename = file.filename.lower()
            
            # To simulate file extraction we need paths, so we save to temporary files
            import tempfile
            import os
            
            suffix = os.path.splitext(filename)[1]
            if not suffix: suffix = '.txt'
                
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(content)
                tmp.flush()
                tmp_path = tmp.name
                
            try:
                if suffix == '.pdf':
                    text = extract_text_from_pdf(tmp_path)
                elif suffix == '.docx':
                    text = extract_text_from_docx(tmp_path)
                else:
                    text = extract_text_from_txt(tmp_path)
                return text
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

        text1 = await extract_text(file1)
        text2 = await extract_text(file2)
        
        # Preprocess
        cleaned1 = preprocess_text(text1)
        cleaned2 = preprocess_text(text2)
        
        # Compare
        score = calculate_similarity(cleaned1, cleaned2)
        risk_level, _ = classify_risk(score)
        
        return DirectCompareResponse(
            file1_name=file1.filename,
            file2_name=file2.filename,
            student1_id=student_id_1,
            student2_id=student_id_2,
            assignment_id=assignment_id,
            score=score,
            score_percentage=score * 100.0,
            risk_level=risk_level,
            message="Comparison successful (on-the-fly)"
        )
        
    except Exception as e:
        logger.error(f"Error in direct comparison: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ====== Individual Endpoints ======

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    assignment_id: int = Form(...),
    student_id: int = Form(...),
    db=Depends(get_db)
):
    """
    Upload a single file and create document record.
    Use this if you want to separate upload from plagiarism check.
    """
    try:
        # Validate that the assignment exists
        cursor = db.cursor()
        cursor.execute("SELECT 1 FROM Assignment WHERE assignment_id = %s", (assignment_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Assignment {assignment_id} not found")
            
        # Validate that the student exists
        cursor.execute("SELECT 1 FROM User WHERE user_id = %s AND role = 'student'", (student_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")

        # Create submission
        cursor.execute(
            "INSERT INTO Submission (assignment_id, student_id) VALUES (%s, %s)",
            (assignment_id, student_id)
        )
        db.commit()
        submission_id = cursor.lastrowid
        
        # Upload file
        file_service = FileService()
        file_path, file_hash = await file_service.save_upload(file, submission_id)
        
        # Create document record
        cursor.execute(
            """INSERT INTO Document (submission_id, file_name, file_path, file_hash) 
               VALUES (%s, %s, %s, %s)""",
            (submission_id, file.filename, file_path, file_hash)
        )
        db.commit()
        document_id = cursor.lastrowid
        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Document WHERE document_id = %s", (document_id,))
        doc = cursor.fetchone()
        
        return FileUploadResponse(
            document_id=doc['document_id'],
            file_name=doc['file_name'],
            file_path=doc['file_path'],
            file_hash=doc['file_hash'],
            uploaded_at=doc['uploaded_at']
        )
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plagiarism-check/{document_id}", response_model=PlagiarismCheckResponse)
async def check_plagiarism_only(
    document_id: int,
    algorithm_id: int = 1,
    db=Depends(get_db)
):
    """
    Run plagiarism check on an already uploaded document.
    """
    try:
        plag_service = PlagiarismService(db)
        
        # Get document info
        doc_info = plag_service.get_document_info(document_id)
        assignment_id = doc_info['assignment_id']
        
        # Run check
        similarity_results = plag_service.check_plagiarism_for_document(
            document_id,
            algorithm_id
        )
        
        # Build response
        cursor = db.cursor(dictionary=True)
        similarity_responses = []
        
        for sim in similarity_results:
            # Fetch detailed info
            sim_details = plag_service.get_similarity_details(sim['similarity_id'])
            
            # Determine which is the target document and which is the matched document
            is_doc1_target = sim_details['doc1_id'] == document_id
            
            similarity_responses.append(SimilarityResult(
                similarity_id=sim['similarity_id'],
                doc1_id=document_id,
                doc1_name=sim_details['doc1_name'] if is_doc1_target else sim_details['doc2_name'],
                student1_name=f"{sim_details['stu1_first']} {sim_details['stu1_last']}" if is_doc1_target else f"{sim_details['stu2_first']} {sim_details['stu2_last']}",
                doc2_id=sim_details['doc2_id'] if is_doc1_target else sim_details['doc1_id'],
                doc2_name=sim_details['doc2_name'] if is_doc1_target else sim_details['doc1_name'],
                student2_name=f"{sim_details['stu2_first']} {sim_details['stu2_last']}" if is_doc1_target else f"{sim_details['stu1_first']} {sim_details['stu1_last']}",
                score=sim['score'],
                score_percentage=sim['score'] * 100,
                risk_level=classify_risk(sim['score'])[0],
                compared_at=sim_details['compared_at']
            ))
        
        return PlagiarismCheckResponse(
            document_id=document_id,
            file_name=doc_info['file_name'],
            total_comparisons=len(plag_service.get_comparison_documents(assignment_id, document_id)),
            similarities_found=len(similarity_results),
            threshold=settings.SIMILARITY_THRESHOLD,
            results=similarity_responses,
            message=f"Found {len(similarity_results)} potential matches"
        )
        
    except Exception as e:
        logger.error(f"Plagiarism check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-report/{similarity_id}", response_model=ReportResponse)
async def generate_report(
    similarity_id: int,
    generated_by: int = Form(...),
    db=Depends(get_db)
):
    """
    Generate PDF report for a specific similarity record.
    """
    try:
        report_service = ReportService(db)
        report_data = report_service.generate_report(similarity_id, generated_by)
        
        return ReportResponse(
            report_id=report_data['report_id'],
            similarity_id=similarity_id,
            report_url=report_data['report_url'],
            report_pdf_path=report_data['report_pdf_path'],
            summary_notes=report_data['summary_notes'],
            created_at=datetime.now()
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/download/{filename}")
async def download_report(filename: str, db=Depends(get_db)):
    """
    Download a generated PDF report.
    """
    try:
        report_service = ReportService(db)
        file_path = report_service.get_report_file_path(filename)
        
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=filename
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Report not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Report download error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/similarity/{similarity_id}")
async def get_reports_by_similarity(similarity_id: int, db=Depends(get_db)):
    """
    Get all reports generated for a similarity record.
    """
    try:
        report_service = ReportService(db)
        reports = report_service.get_reports_by_similarity(similarity_id)
        return {"reports": reports}
    except Exception as e:
        logger.error(f"Error fetching reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))
