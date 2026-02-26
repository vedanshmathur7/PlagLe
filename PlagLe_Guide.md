# PlagLe User Guide 📚🕵️‍♂️

Welcome to **PlagLe**, your automated Plagiarism Detection and Similarity Tracking System!

This guide explains how PlagLe functions from end-to-end, what files you can upload, and how instructors can use the system to maintain academic integrity.

---

## 1. Supported File Uploads 📁

PlagLe is equipped with a robust text-extraction engine. When students submit assignments, the system automatically reads the raw text from the following document types:

*   **`.TXT` (Plain Text)**: Standard unformatted text documents.
*   **`.PDF` (Portable Document Format)**: Text-based PDF files. *(Note: Scanned images saved as PDFs without OCR text layers are not currently supported).*
*   **`.DOCX` (Microsoft Word)**: Standard modern Microsoft Word documents.

---

## 2. System Workflow (How It Works) ⚙️

PlagLe operates entirely in the background. Here is the lifecycle of a document in the system:

### Phase A: Submission (Students)
1. An **Instructor** creates a `Course` (e.g., *CS101*) and an `Assignment` (e.g., *Final Essay*).
2. **Students** upload their documents (`.pdf`, `.docx`, or `.txt`) to that specific Assignment.
3. The system records the `Submission` and saves the `Document` locally.

### Phase B: Processing & Comparison (System Automation)
1. The moment a new file is uploaded, PlagLe's **Similarity Engine** wakes up.
2. It extracts the raw text and cleans it (converts to lowercase, removes punctuation, and strips out common filler words like "the", "and", "is").
3. PlagLe automatically finds **every other document** submitted by other students for that exact same Assignment.
4. Using an advanced mathematical algorithm (**TF-IDF Cosine Similarity**), the system compares the new document against all older documents.
5. If the system detects a text overlap of **20% or higher** (Score > `0.20`), it permanently records this mathematically linked pair in the secure MySQL `Similarity` database.

### Phase C: Review & Reporting (Instructors)
1. **Instructors** can view matches for their assignments.
2. The system translates the raw math into a human-readable **Risk Level**:
   *   🟢 **Low Risk (20% - 49%)**: Minor overlaps, common phrasing, or templates.
   *   🟠 **Medium Risk (50% - 79%)**: Significant overlap requiring manual review.
   *   🔴 **High Risk (80%+)**: High probability of direct copying or academic dishonesty.
3. The Instructor can trigger the **Report Generator** to output a formal, structured **PDF Report** detailing exactly who matched with whom, for which assignment, right down to the exact percentage score.

---

## 3. Best Practices for Instructors 🎓
*   **Require Text-based Files**: Remind students not to submit screenshot-based PDFs. If you cannot highlight the text in a PDF with your mouse, PlagLe cannot read it either.
*   **Ignore the Noise**: A 25% match is often just students answering the same prompt with similar vocabulary. Focus your administrative time on scores generating **Medium** or **High** Risk reports.
*   **Use the PDF Reports**: Always generate the PDF Report before discussing potential plagiarism with a student to ensure you have a timestamped, system-generated artifact of proof.

---

## 4. Technical Architecture & Database Design 🛠️

*(For Developers & Database Administrators)*

### A. The End-to-End System Flow ⚙️
1. **Hierarchy Setup**: An Instructor creates a **Course** and an **Assignment**. A Student makes a **Submission** and uploads a **Document** (PDF, DOCX, or TXT).
2. **Text Extraction & Caching**: The system intercepts the document, extracts the raw strings (using `PyPDF2` or `docx`), removes punctuation, and strips out "stopwords" (useless words like "the", "and") using `NLTK`. It saves this cleaned text back to the database to avoid expensive re-reads later.
3. **Targeted Fetching**: When a document is uploaded, the script (`automation.py`) queries the database to find **all other documents submitted for that exact same Assignment**. 
4. **The Math Engine**: It compares the newly uploaded document's text against the other documents using **TF-IDF Cosine Similarity**. 
5. **Thresholding & Reporting**: If the similarity score is above 20% (0.20), it records the match in the `Similarity` table. Later, an instructor can generate a PDF report that does a massive SQL `JOIN` to pull the student names, course names, and similarity score into a printable format.

### B. Similarity Mathematics & `doc_id` 🔍
* **The Math (TF-IDF & Cosine Similarity):** 
  Instead of doing a basic word-for-word match, the system converts documents into numerical vectors using **TF-IDF** (Term Frequency-Inverse Document Frequency). This gives higher mathematical weight to unique, specific words and lower weight to common words. It then calculates the **Cosine Similarity** (the angle between these two vectors). A score of 0.0 means completely different, and 1.0 means identical.
* **How `doc_id` Works:** 
  Every document gets an Auto-Incremented `document_id`. If `doc_id = 5` is uploaded, it gets compared to older documents in the same assignment (e.g., `doc_id` 1, 2, and 4). 
* **The "Mirror Duplicate" Problem:**
  If you compare `doc 2` and `doc 5`, you do not want to store one row for `(2, 5)` and another row for `(5, 2)`. The system uses `min()` and `max()` to strictly ensure the smaller ID is always `doc1_id` and the larger is `doc2_id`.

### C. Advanced MySQL Usage (DBMS Concepts) 🗄️
* **Highly Normalized Schema (3NF):** We designed 8 distinct tables (`User`, `Course`, `Assignment`, `Submission`, `Document`, `Algorithm`, `Similarity`, `Report`). There is no data redundancy. The `Similarity` table only stores IDs, relying on relational joins to get user data.
* **Referential Integrity & Cascading:** We heavily utilized `FOREIGN KEY` constraints with `ON DELETE CASCADE`. If a Course is deleted, all related Assignments, Submissions, Documents, and Similarity scores are automatically cleaned up.
* **Smart Constraints:** 
  * `CHECK (doc1_id < doc2_id)`: Physically prevents the database from storing mirror duplicates. 
  * `UNIQUE (doc1_id, doc2_id, algorithm_id)`: Ensures the same two documents can never be compared duplicate times by the same algorithm.
* **Heavy SQL Joins for Reporting:** The Report Generator utilizes a massive, optimized **7-table JOIN query** starting from the `Similarity` table all the way to `Course` to fetch the entire context in one fast database trip.
* **Strategic Indexing:** Indexes like `CREATE INDEX idx_similarity_score ON Similarity(score DESC);` allow the system to instantly pull the highest-risk plagiarism cases without scanning the whole table.
