# OS and time utilities
import os
from datetime import datetime

# ReportLab for creating PDF canvases and defining page sizes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Database connection
import mysql.connector

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

# 1. Fetch similarity records
def get_similarity_data(db, similarity_id):
    """
    2. Join Tables: Similarity, Document, Submission, User, Assignment, Algorithm
    Fetches the full context required for a single report.
    """
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            sim.similarity_id, sim.score, sim.compared_at,
            alg.name AS algorithm_name,
            
            d1.file_name AS doc1_name, d1.file_path AS doc1_path,
            u1.first_name AS stu1_first, u1.last_name AS stu1_last,
            
            d2.file_name AS doc2_name, d2.file_path AS doc2_path,
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
        
        -- Both belong to the same assignment, so we just join on s1's assignment
        JOIN Assignment a ON s1.assignment_id = a.assignment_id
        JOIN Course c ON a.course_id = c.course_id
        
        WHERE sim.similarity_id = %s
    """
    cursor.execute(query, (similarity_id,))
    return cursor.fetchone()

# 3. Classify Risk
# Slots aligned with SIMILARITY_THRESHOLD=0.15:
#   0.00 – 0.15  → never surfaced (below detection threshold)
#   0.15 – 0.35  → Low Risk    (flagged but minor overlap)
#   0.35 – 0.60  → Medium Risk (notable similarity, review needed)
#   0.60 – 1.00  → High Risk   (strong overlap, likely plagiarism)
def classify_risk(score):
    if score < 0.35:
        return "Low Risk", "Green"
    elif score < 0.60:
        return "Medium Risk", "Orange"
    else:
        return "High Risk", "Red"

# 4 & 6. Generate Textual/PDF Report
def generate_pdf_report(data, generated_by_user_id):
    score_pct = data['score'] * 100
    risk_level, color = classify_risk(data['score'])
    
    # Define file path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"reports/Report_SIM{data['similarity_id']}_{timestamp}.pdf"
    
    # Initialize Canvas
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "PlagLe - Plagiarism Detection Report")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 85, f"Course: {data['course_code']} | Assignment: {data['assignment_title']}")
    
    c.line(50, height - 100, width - 50, height - 100)
    
    # Body
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 130, "Comparison Summary")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 160, f"Document 1: {data['doc1_name']} (Student: {data['stu1_first']} {data['stu1_last']})")
    c.drawString(50, height - 180, f"Document 2: {data['doc2_name']} (Student: {data['stu2_first']} {data['stu2_last']})")
    
    c.drawString(50, height - 210, f"Algorithm Used: {data['algorithm_name']}")
    c.drawString(50, height - 230, f"Compared At: {data['compared_at']}")
    
    # Results Highlighting
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 270, f"Similarity Score: {score_pct:.2f}%")
    
    c.drawString(50, height - 290, f"Interpretation: {risk_level}")
    
    # System Notes
    c.setFont("Helvetica-Oblique", 10)
    notes = f"This report indicates a {risk_level} of academic dishonesty based on pure text overlap."
    c.drawString(50, height - 330, "System Notes: " + notes)
    
    c.save()
    print(f"PDF Report generated successfully: {pdf_filename}")
    
    return pdf_filename, notes

# 5. Insert Report Metadata into DB
def save_report_to_db(db, similarity_id, generated_by, notes, pdf_path):
    cursor = db.cursor()
    query = """
        INSERT INTO Report (similarity_id, generated_by, summary_notes, report_pdf_path)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (similarity_id, generated_by, notes, pdf_path))
    db.commit()
    print(f">>> SUCCESS: Report metadata saved to DB (Similarity ID: {similarity_id})")

# 7. Full Test Flow
def run_report_pipeline(db, similarity_id, instructor_id):
    print(f"\n--- Starting Report Generation for Similarity ID: {similarity_id} ---")
    
    # Step 2: Fetch Data
    data = get_similarity_data(db, similarity_id)
    if not data:
        print("Error: Similarity record not found.")
        return
        
    # Step 4 & 6: Generate PDF
    pdf_path, system_notes = generate_pdf_report(data, instructor_id)
    
    # Step 5: Save to DB
    save_report_to_db(db, similarity_id, instructor_id, system_notes, pdf_path)
    
    print("--- Report Generation Complete ---\n")

# To run locally if called directly
if __name__ == "__main__":
    from automation import get_db_connection
    db_conn = get_db_connection()
    if db_conn:
        # Assumes Similarity ID 1 and User ID 1 (Instructor) exist from earlier tests
        run_report_pipeline(db_conn, similarity_id=1, instructor_id=1)
