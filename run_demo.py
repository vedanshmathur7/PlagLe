import os
import sys
import mysql.connector

# Add current dir to path to import modules
sys.path.append(os.getcwd())

from automation import get_db_connection, process_new_document
from report_generator import run_report_pipeline

def setup_demo():
    db = get_db_connection()
    if not db:
        print("Failed to connect to DB.")
        return
        
    cursor = db.cursor()

    try:
        # Insert Algorithm
        cursor.execute("INSERT IGNORE INTO Algorithm (algorithm_id, name, version, description) VALUES (1, 'TF-IDF Cosine Simple', '1.0', 'Basic text matcher')")
        
        # Insert Users
        cursor.execute("INSERT IGNORE INTO User (user_id, first_name, last_name, email, password_hash, role) VALUES (1, 'Prof', 'Smith', 'smith@uni.edu', 'hash', 'instructor')")
        cursor.execute("INSERT IGNORE INTO User (user_id, first_name, last_name, email, password_hash, role) VALUES (2, 'Alice', 'A', 'alice@uni.edu', 'hash', 'student')")
        cursor.execute("INSERT IGNORE INTO User (user_id, first_name, last_name, email, password_hash, role) VALUES (3, 'Bob', 'B', 'bob@uni.edu', 'hash', 'student')")
        cursor.execute("INSERT IGNORE INTO User (user_id, first_name, last_name, email, password_hash, role) VALUES (4, 'Charlie', 'C', 'charlie@uni.edu', 'hash', 'student')")
        
        # Insert Course
        cursor.execute("INSERT IGNORE INTO Course (course_id, course_code, course_name, instructor_id) VALUES (1, 'CS101', 'Intro to CS', 1)")
        
        # Insert Assignment
        cursor.execute("INSERT IGNORE INTO Assignment (assignment_id, course_id, title, due_date) VALUES (1, 1, 'Final Essay', '2026-12-31 23:59:59')")
        
        # Insert Submissions
        cursor.execute("INSERT IGNORE INTO Submission (submission_id, assignment_id, student_id) VALUES (1, 1, 2)")
        cursor.execute("INSERT IGNORE INTO Submission (submission_id, assignment_id, student_id) VALUES (2, 1, 3)")
        cursor.execute("INSERT IGNORE INTO Submission (submission_id, assignment_id, student_id) VALUES (3, 1, 4)")
        
        # Insert Documents with absolute paths
        pathA = os.path.abspath('doc_A.txt')
        pathB = os.path.abspath('doc_B.txt')
        pathC = os.path.abspath('doc_C.txt')
        
        cursor.execute("REPLACE INTO Document (document_id, submission_id, file_name, file_path, file_hash) VALUES (1, 1, 'doc_A.txt', %s, 'hashA')", (pathA,))
        cursor.execute("REPLACE INTO Document (document_id, submission_id, file_name, file_path, file_hash) VALUES (2, 2, 'doc_B.txt', %s, 'hashB')", (pathB,))
        cursor.execute("REPLACE INTO Document (document_id, submission_id, file_name, file_path, file_hash) VALUES (3, 3, 'doc_C.txt', %s, 'hashC')", (pathC,))
        
        # Clear out any empty extracted text so it gets re-extracted
        cursor.execute("UPDATE Document SET extracted_text = NULL")
        
        db.commit()
        print("Test data inserted successfully.")
    except Exception as e:
        print(f"Error inserting test data: {e}")
        db.rollback()

    print("\n--- Running Automation ---")
    process_new_document(db, 1)
    process_new_document(db, 2)
    process_new_document(db, 3)

    print("\n--- Generating Reports ---")
    cursor.execute("SELECT similarity_id FROM Similarity")
    sims = cursor.fetchall()
    if not sims:
        print("No similarities found above threshold.")
    for sim in sims:
        run_report_pipeline(db, sim[0], 1)

    db.close()
    
if __name__ == "__main__":
    setup_demo()
