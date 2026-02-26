import mysql.connector
from mysql.connector import Error
import os
from similarity_engine import (
    extract_text_from_txt,
    extract_text_from_pdf,
    extract_text_from_docx,
    preprocess_text,
    calculate_similarity
)

# 1. Connect to MySQL safely
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='PlagLe', # Adjust with actual database name if different
            user='root',
            password='1234'   # Adjust with actual password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Utility: Extract text based on file extension
def extract_text(file_path):
    if not os.path.exists(file_path):
        return ""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        return extract_text_from_txt(file_path)

# 2. Fetch document details by ID
def get_document_by_id(db, document_id):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Document WHERE document_id = %s"
    cursor.execute(query, (document_id,))
    return cursor.fetchone()

# 3. Fetch all other documents for the same assignment
def get_other_documents_in_assignment(db, assignment_id, exclude_document_id):
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT d.* FROM Document d
        JOIN Submission s ON d.submission_id = s.submission_id
        WHERE s.assignment_id = %s AND d.document_id != %s
    """
    cursor.execute(query, (assignment_id, exclude_document_id))
    return cursor.fetchall()

# 4. Extract text if not stored, update Document.extracted_text
def get_or_extract_text(db, document):
    # Check if 'extracted_text' column has data
    if document.get('extracted_text'):
        return document['extracted_text']
    
    # Otherwise, extract it
    print(f"Extracting text dynamically for Document ID: {document['document_id']}...")
    text = extract_text(document['file_path'])
    
    if text:
        cursor = db.cursor()
        update_query = "UPDATE Document SET extracted_text = %s WHERE document_id = %s"
        cursor.execute(update_query, (text, document['document_id']))
        db.commit()
        
    return text

# Main Automation Flow (Steps 5-9)
def process_new_document(db, new_document_id):
    print(f"\n--- Starting Processing for New Document ID: {new_document_id} ---")
    
    # Fetch new document
    new_doc = get_document_by_id(db, new_document_id)
    if not new_doc:
        print("New document not found!")
        return
        
    # Find assignment_id via submission_id
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT assignment_id FROM Submission WHERE submission_id = %s", (new_doc['submission_id'],))
    sub = cursor.fetchone()
    if not sub:
        print("Submission not found for document!")
        return
        
    assignment_id = sub['assignment_id']
    
    # Step 4: Extract/Get text for new doc
    new_text = get_or_extract_text(db, new_doc)
    if not new_text:
        print("Failed to extract text from new document. Aborting comparison.")
        return
    
    new_cleaned = preprocess_text(new_text)

    # Step 3: Fetch existing documents
    existing_docs = get_other_documents_in_assignment(db, assignment_id, new_document_id)
    print(f"Found {len(existing_docs)} other document(s) in Assignment {assignment_id} to compare against.")

    # Assume Algorithm ID 1 is standard TF-IDF Cosine Similarity
    algorithm_id = 1 
    threshold = 0.20 # Step 6: Threshold logic

    for existing_doc in existing_docs:
        print(f"\nComparing Doc {new_document_id} vs Doc {existing_doc['document_id']}...")
        
        # Step 4: Extract/Get text for existing doc
        existing_text = get_or_extract_text(db, existing_doc)
        existing_cleaned = preprocess_text(existing_text)

        # Step 5: Integrate similarity engine
        score = calculate_similarity(new_cleaned, existing_cleaned)
        print(f"Calculated Score: {score:.4f}")

        # Step 6: Threshold check
        if score > threshold:
            # Step 7: Ensure doc1_id < doc2_id and avoid duplicates
            doc1_id = min(new_document_id, existing_doc['document_id'])
            doc2_id = max(new_document_id, existing_doc['document_id'])
            
            # Check if entry already exists
            cursor.execute("""
                SELECT similarity_id FROM Similarity 
                WHERE doc1_id = %s AND doc2_id = %s AND algorithm_id = %s
            """, (doc1_id, doc2_id, algorithm_id))
            
            if cursor.fetchone():
                print(f"Similarity record already exists for Docs ({doc1_id}, {doc2_id}). Skipping insertion.")
            else:
                # Step 8: Insert similarity result
                insert_query = """
                    INSERT INTO Similarity (doc1_id, doc2_id, algorithm_id, score)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (doc1_id, doc2_id, algorithm_id, float(score)))
                db.commit()
                # Step 9: Print confirmation log
                print(f">>> SUCCESS: Inserted valid Similarity Score {score:.4f} for Docs ({doc1_id}, {doc2_id}).")
        else:
            print(f"Score {score:.4f} is below threshold ({threshold}). Ignored.")

    print(f"--- Finished Processing for Document ID: {new_document_id} ---\n")
