"""
Plagiarism Service - Wraps similarity_engine.py with database operations
"""
import logging
from typing import List, Dict, Any
import mysql.connector

# Import our existing plagiarism detection engine
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.utils.similarity_engine import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_docx,
    preprocess_text,
    calculate_similarity
)

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PlagiarismService:
    """
    Service layer for plagiarism detection.
    Wraps the core similarity_engine functions with database operations.
    """
    
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
        self.cursor = self.db.cursor(dictionary=True)
    
    def extract_text_from_document(self, file_path: str) -> str:
        """
        Extract text from a document based on file extension.
        Wrapper around similarity_engine extraction functions.
        """
        try:
            if file_path.endswith('.pdf'):
                return extract_text_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return extract_text_from_docx(file_path)
            else:  # .txt or default
                return extract_text_from_txt(file_path)
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            raise
    
    def store_extracted_text(self, document_id: int, text: str) -> None:
        """
        Store extracted text in database for caching.
        """
        # Add extracted_text column if it exists in your schema
        # For now, we'll just log
        logger.info(f"Extracted {len(text)} characters from document {document_id}")
    
    def get_document_info(self, document_id: int) -> Dict[str, Any]:
        """Fetch document information from database"""
        query = """
            SELECT d.*, s.student_id, s.assignment_id
            FROM Document d
            JOIN Submission s ON d.submission_id = s.submission_id
            WHERE d.document_id = %s
        """
        self.cursor.execute(query, (document_id,))
        result = self.cursor.fetchone()
        
        if not result:
            raise ValueError(f"Document {document_id} not found")
        
        return result
    
    def get_comparison_documents(self, assignment_id: int, current_doc_id: int) -> List[Dict[str, Any]]:
        """
        Get all documents from the same assignment for comparison.
        Excludes the current document.
        """
        query = """
            SELECT d.document_id, d.file_name, d.file_path, s.student_id
            FROM Document d
            JOIN Submission s ON d.submission_id = s.submission_id
            WHERE s.assignment_id = %s 
            AND d.document_id != %s
            ORDER BY d.document_id
        """
        self.cursor.execute(query, (assignment_id, current_doc_id))
        return self.cursor.fetchall()
    
    def compare_documents(
        self, 
        doc1_id: int, 
        doc2_id: int, 
        algorithm_id: int
    ) -> float:
        """
        Compare two documents and return similarity score.
        Uses the core similarity_engine logic.
        """
        # Get document paths
        doc1 = self.get_document_info(doc1_id)
        doc2 = self.get_document_info(doc2_id)
        
        # Extract text
        text1 = self.extract_text_from_document(doc1['file_path'])
        text2 = self.extract_text_from_document(doc2['file_path'])
        
        # Preprocess
        cleaned1 = preprocess_text(text1)
        cleaned2 = preprocess_text(text2)
        
        # Calculate similarity
        score = calculate_similarity(cleaned1, cleaned2)
        
        logger.info(f"Similarity between docs {doc1_id} and {doc2_id}: {score:.4f}")
        
        return score
    
    def save_similarity_result(
        self, 
        doc1_id: int, 
        doc2_id: int, 
        algorithm_id: int, 
        score: float
    ) -> int:
        """
        Save similarity result to database.
        Returns similarity_id.
        """
        # Ensure doc1_id < doc2_id (database constraint)
        if doc1_id > doc2_id:
            doc1_id, doc2_id = doc2_id, doc1_id
        
        query = """
            INSERT INTO Similarity (doc1_id, doc2_id, algorithm_id, score)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                score = VALUES(score),
                compared_at = CURRENT_TIMESTAMP
        """
        
        try:
            self.cursor.execute(query, (doc1_id, doc2_id, algorithm_id, score))
            self.db.commit()
            
            # Get the similarity_id
            similarity_id = self.cursor.lastrowid
            if similarity_id == 0:  # Update case, fetch existing ID
                self.cursor.execute(
                    "SELECT similarity_id FROM Similarity WHERE doc1_id=%s AND doc2_id=%s AND algorithm_id=%s",
                    (doc1_id, doc2_id, algorithm_id)
                )
                result = self.cursor.fetchone()
                similarity_id = result['similarity_id']
            
            logger.info(f"Saved similarity_id: {similarity_id}")
            return similarity_id
            
        except mysql.connector.Error as err:
            logger.error(f"Database error saving similarity: {err}")
            self.db.rollback()
            raise
    
    def check_plagiarism_for_document(
        self, 
        document_id: int, 
        algorithm_id: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Check plagiarism for a document against all others in same assignment.
        Returns list of similarity results above threshold.
        """
        results = []
        
        # Get document info
        doc_info = self.get_document_info(document_id)
        assignment_id = doc_info['assignment_id']
        
        # Get all other documents in assignment
        comparison_docs = self.get_comparison_documents(assignment_id, document_id)
        
        if not comparison_docs:
            logger.info(f"No other documents to compare for document {document_id}")
            return results
        
        logger.info(f"Comparing document {document_id} against {len(comparison_docs)} documents")
        
        # Compare with each document
        for comp_doc in comparison_docs:
            try:
                score = self.compare_documents(document_id, comp_doc['document_id'], algorithm_id)
                
                # Save to database
                similarity_id = self.save_similarity_result(
                    document_id,
                    comp_doc['document_id'],
                    algorithm_id,
                    score
                )
                
                # Only return if above threshold
                if score >= settings.SIMILARITY_THRESHOLD:
                    results.append({
                        'similarity_id': similarity_id,
                        'doc1_id': min(document_id, comp_doc['document_id']),
                        'doc2_id': max(document_id, comp_doc['document_id']),
                        'score': score,
                        'compared_doc': comp_doc
                    })
                    
            except Exception as e:
                logger.error(f"Error comparing documents: {e}")
                continue
        
        logger.info(f"Found {len(results)} similarities above threshold for document {document_id}")
        return results
    
    def get_similarity_details(self, similarity_id: int) -> Dict[str, Any]:
        """
        Get full details of a similarity record for report generation.
        """
        query = """
            SELECT 
                sim.similarity_id, sim.score, sim.compared_at,
                alg.name AS algorithm_name,
                
                d1.document_id AS doc1_id, d1.file_name AS doc1_name, 
                d1.file_path AS doc1_path,
                u1.first_name AS stu1_first, u1.last_name AS stu1_last,
                
                d2.document_id AS doc2_id, d2.file_name AS doc2_name, 
                d2.file_path AS doc2_path,
                u2.first_name AS stu2_first, u2.last_name AS stu2_last,
                
                a.title AS assignment_title, c.course_code
                
            FROM Similarity sim
            JOIN Algorithm alg ON sim.algorithm_id = alg.algorithm_id
            
            JOIN Document d1 ON sim.doc1_id = d1.document_id
            JOIN Submission s1 ON d1.submission_id = s1.submission_id
            JOIN User u1 ON s1.student_id = u1.user_id
            
            JOIN Document d2 ON sim.doc2_id = d2.document_id
            JOIN Submission s2 ON d2.submission_id = s2.submission_id
            JOIN User u2 ON s2.student_id = u2.user_id
            
            JOIN Assignment a ON s1.assignment_id = a.assignment_id
            JOIN Course c ON a.course_id = c.course_id
            
            WHERE sim.similarity_id = %s
        """
        
        self.cursor.execute(query, (similarity_id,))
        result = self.cursor.fetchone()
        
        if not result:
            raise ValueError(f"Similarity {similarity_id} not found")
        
        return result
