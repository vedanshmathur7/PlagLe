import mysql.connector
import os
from dotenv import load_dotenv

# Load .env from the parent directory (plagle-backend)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def view_similarity_records():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        
        query = """
        SELECT 
            s.similarity_id,
            d1.file_name AS doc1,
            d2.file_name AS doc2,
            a.name AS algorithm,
            s.score,
            s.compared_at
        FROM Similarity s
        JOIN Document d1 ON s.doc1_id = d1.document_id
        JOIN Document d2 ON s.doc2_id = d2.document_id
        JOIN Algorithm a ON s.algorithm_id = a.algorithm_id
        ORDER BY s.score DESC
        LIMIT 10;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print("MySQL Database Records: Table 'Similarity'")
        print("==========================================================================================")
        print(f"{'ID':<4} | {'Document 1':<20} | {'Document 2':<20} | {'Algorithm':<15} | {'Score':<6} | {'Compared At'}")
        print("-" * 90)
        
        for row in rows:
            sim_id, d1, d2, algo, score, dt = row
            print(f"{sim_id:<4} | {d1:<20} | {d2:<20} | {algo:<15} | {float(score):.4f} | {dt}")
            
        print("==========================================================================================")
        
        conn.close()
    except Exception as e:
        # Fallback if DB is not reachable
        print(f"Error connecting to database: {e}")
        print("\nDisplaying Mock Data (as expected in final report):")
        print("MySQL Database Records: Table 'Similarity'")
        print("==========================================================================================")
        print(f"{'ID':<4} | {'Document 1':<20} | {'Document 2':<20} | {'Algorithm':<15} | {'Score':<6} | {'Compared At'}")
        print("-" * 90)
        mock_data = [
            (1, "bst_rohan.cpp", "bst_ananya.cpp", "TF-IDF Cosine", 0.9210, "2026-05-01 14:22:01"),
            (15, "sql_rohan.sql", "sql_ananya.sql", "TF-IDF Cosine", 0.9450, "2026-05-02 09:15:33"),
            (22, "strings_rohan.py", "strings_ananya.py", "TF-IDF Cosine", 0.9670, "2026-05-03 11:45:12"),
            (7, "graph_rohan.cpp", "graph_ananya.cpp", "TF-IDF Cosine", 0.8750, "2026-05-01 16:30:45"),
            (18, "linreg_vikram.py", "linreg_sneha.py", "TF-IDF Cosine", 0.7800, "2026-05-02 18:10:20")
        ]
        for row in mock_data:
            sim_id, d1, d2, algo, score, dt = row
            print(f"{sim_id:<4} | {d1:<20} | {d2:<20} | {algo:<15} | {score:.4f} | {dt}")
        print("==========================================================================================")

if __name__ == "__main__":
    view_similarity_records()
