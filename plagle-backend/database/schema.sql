-- PlagLe: Database Schema

-- 1. User Table
CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'instructor', 'admin') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Course Table
CREATE TABLE Course (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(20) NOT NULL UNIQUE,
    course_name VARCHAR(100) NOT NULL,
    instructor_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- 3. Assignment Table
CREATE TABLE Assignment (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    due_date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE
);

-- 4. Submission Table
CREATE TABLE Submission (
    submission_id INT AUTO_INCREMENT PRIMARY KEY,
    assignment_id INT NOT NULL,
    student_id INT NOT NULL,
    attempt_number INT DEFAULT 1,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assignment_id) REFERENCES Assignment(assignment_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- 5. Document Table
CREATE TABLE Document (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    submission_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_hash VARCHAR(64) NOT NULL, 
    extracted_text TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (submission_id) REFERENCES Submission(submission_id) ON DELETE CASCADE
);

-- 6. Algorithm Table
CREATE TABLE Algorithm (
    algorithm_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    version VARCHAR(20) NOT NULL,
    description TEXT
);

-- 7. Similarity Table
CREATE TABLE Similarity (
    similarity_id INT AUTO_INCREMENT PRIMARY KEY,
    doc1_id INT NOT NULL,
    doc2_id INT NOT NULL,
    algorithm_id INT NOT NULL,
    score DECIMAL(5,4) NOT NULL,
    compared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doc1_id) REFERENCES Document(document_id) ON DELETE CASCADE,
    FOREIGN KEY (doc2_id) REFERENCES Document(document_id) ON DELETE CASCADE,
    FOREIGN KEY (algorithm_id) REFERENCES Algorithm(algorithm_id) ON DELETE CASCADE,
    CONSTRAINT chk_doc_order CHECK (doc1_id < doc2_id),
    CONSTRAINT uq_similarity_comparison UNIQUE (doc1_id, doc2_id, algorithm_id)
);

-- 8. Report Table
CREATE TABLE Report (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    similarity_id INT NOT NULL,
    generated_by INT NOT NULL,
    summary_notes TEXT,
    report_pdf_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (similarity_id) REFERENCES Similarity(similarity_id) ON DELETE CASCADE,
    FOREIGN KEY (generated_by) REFERENCES User(user_id) ON DELETE RESTRICT
);

-- Indexes
CREATE INDEX idx_submission_assignment ON Submission(assignment_id);
CREATE INDEX idx_submission_student_assignment ON Submission(student_id, assignment_id);
CREATE INDEX idx_document_hash ON Document(file_hash);
CREATE INDEX idx_similarity_score ON Similarity(score DESC);
