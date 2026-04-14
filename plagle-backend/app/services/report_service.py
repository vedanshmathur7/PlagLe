"""
Report Service - Wraps report_generator.py with async-safe operations
"""
import logging
from typing import Dict, Any
import mysql.connector

# Import existing report generation logic
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.utils.report_generator import classify_risk, generate_pdf_report

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ReportService:
    """
    Service layer for report generation.
    Wraps the core report_generator functions with database operations.
    """
    
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
        self.cursor = self.db.cursor(dictionary=True)
    
    def generate_report(
        self, 
        similarity_id: int, 
        generated_by: int
    ) -> Dict[str, Any]:
        """
        Generate PDF report for a similarity record.
        Returns report metadata.
        """
        # Import here to use the existing function
        from app.services.plagiarism_service import PlagiarismService
        
        # Get similarity details
        plag_service = PlagiarismService(self.db)
        similarity_data = plag_service.get_similarity_details(similarity_id)
        
        if not similarity_data:
            raise ValueError(f"Similarity {similarity_id} not found")
        
        logger.info(f"Generating report for similarity {similarity_id}")
        
        # Generate PDF using existing function
        pdf_path, system_notes = generate_pdf_report(similarity_data, generated_by)
        
        # Save to database
        report_id = self._save_report_metadata(
            similarity_id, 
            generated_by, 
            system_notes, 
            pdf_path
        )
        
        # Construct report URL (for frontend access)
        report_filename = os.path.basename(pdf_path)
        report_url = f"/api/v1/reports/download/{report_filename}"
        
        return {
            'report_id': report_id,
            'similarity_id': similarity_id,
            'report_url': report_url,
            'report_pdf_path': pdf_path,
            'summary_notes': system_notes,
            'score': similarity_data['score'],
            'risk_level': classify_risk(similarity_data['score'])[0]
        }
    
    def _save_report_metadata(
        self, 
        similarity_id: int, 
        generated_by: int, 
        notes: str, 
        pdf_path: str
    ) -> int:
        """
        Save report metadata to database.
        Returns report_id.
        """
        query = """
            INSERT INTO Report (similarity_id, generated_by, summary_notes, report_pdf_path)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            self.cursor.execute(query, (similarity_id, generated_by, notes, pdf_path))
            self.db.commit()
            report_id = self.cursor.lastrowid
            
            logger.info(f"Report saved with ID: {report_id}")
            return report_id
            
        except mysql.connector.Error as err:
            logger.error(f"Database error saving report: {err}")
            self.db.rollback()
            raise
    
    def get_report_by_id(self, report_id: int) -> Dict[str, Any]:
        """Fetch report metadata by ID"""
        query = """
            SELECT r.*, sim.score, 
                   d1.file_name AS doc1_name, d2.file_name AS doc2_name
            FROM Report r
            JOIN Similarity sim ON r.similarity_id = sim.similarity_id
            JOIN Document d1 ON sim.doc1_id = d1.document_id
            JOIN Document d2 ON sim.doc2_id = d2.document_id
            WHERE r.report_id = %s
        """
        
        self.cursor.execute(query, (report_id,))
        result = self.cursor.fetchone()
        
        if not result:
            raise ValueError(f"Report {report_id} not found")
        
        return result
    
    def get_reports_by_similarity(self, similarity_id: int) -> list:
        """Get all reports for a similarity record"""
        query = """
            SELECT * FROM Report
            WHERE similarity_id = %s
            ORDER BY created_at DESC
        """
        
        self.cursor.execute(query, (similarity_id,))
        return self.cursor.fetchall()
    
    def get_report_file_path(self, filename: str) -> str:
        """
        Get full file path for a report filename.
        Validates that the file exists in the reports directory.
        """
        # Security: Only allow files from reports directory
        file_path = os.path.join(settings.REPORT_DIR, filename)
        abs_path = os.path.abspath(file_path)
        
        # Ensure the path is within reports directory
        reports_dir = os.path.abspath(settings.REPORT_DIR)
        if not abs_path.startswith(reports_dir):
            raise ValueError("Invalid report path")
        
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Report file not found: {filename}")
        
        return abs_path
