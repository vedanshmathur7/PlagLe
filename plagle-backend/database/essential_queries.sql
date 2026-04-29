-- ==============================================================================
-- PLAGLE DBMS PROJECT - ADVANCED SQL COMPONENTS (VIVA DEMONSTRATION)
-- ==============================================================================
-- This file contains all the advanced database components required for the viva.
-- You can run this entire file in MySQL Workbench, or copy-paste components
-- directly into your MySQL terminal.
-- Example usages are provided as comments at the end of each section.

-- ------------------------------------------------------------------------------
-- 1. STORED PROCEDURE
-- ------------------------------------------------------------------------------
-- Purpose: Retrieves a specific student's complete similarity report.
-- ------------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS GetStudentReport;

DELIMITER //
CREATE PROCEDURE GetStudentReport(IN studentID INT)
BEGIN
    SELECT a.title AS assignment, d.file_name, s.score
    FROM Similarity s
    JOIN Document d ON (s.doc1_id = d.document_id OR s.doc2_id = d.document_id)
    JOIN Submission sub ON d.submission_id = sub.submission_id
    JOIN Assignment a ON sub.assignment_id = a.assignment_id
    WHERE sub.student_id = studentID;
END //
DELIMITER ;

-- [EXAMPLE USAGE IN MYSQL TERMINAL]
-- Type this exactly in your MySQL terminal to see Student #1's report:
-- CALL GetStudentReport(1);


-- ------------------------------------------------------------------------------
-- 2. VIEWS & JOINS
-- ------------------------------------------------------------------------------
-- Purpose: A complex 6-table JOIN saved as a View to easily monitor high-risk plagiarism.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW HighRiskPlagiarism AS
SELECT 
    s.similarity_id,
    s.score,
    d1.file_name AS doc1,
    u1.first_name AS student1,
    d2.file_name AS doc2,
    u2.first_name AS student2
FROM Similarity s
JOIN Document d1 ON s.doc1_id = d1.document_id
JOIN Submission sub1 ON d1.submission_id = sub1.submission_id
JOIN User u1 ON sub1.student_id = u1.user_id
JOIN Document d2 ON s.doc2_id = d2.document_id
JOIN Submission sub2 ON d2.submission_id = sub2.submission_id
JOIN User u2 ON sub2.student_id = u2.user_id
WHERE s.score >= 0.15;

-- [EXAMPLE USAGE IN MYSQL TERMINAL]
-- Type this to see all flagged high-risk similarities:
-- SELECT * FROM HighRiskPlagiarism;


-- ------------------------------------------------------------------------------
-- 3. GROUP BY + HAVING
-- ------------------------------------------------------------------------------
-- Purpose: Saved as a View to find assignments that have more than 5 submissions.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW PopularAssignments AS
SELECT assignment_id, COUNT(submission_id) AS total_submissions
FROM Submission
GROUP BY assignment_id
HAVING COUNT(submission_id) > 5;

-- [EXAMPLE USAGE IN MYSQL TERMINAL]
-- Type this to see assignments with >5 submissions:
-- SELECT * FROM PopularAssignments;


-- ------------------------------------------------------------------------------
-- 4. SUBQUERIES
-- ------------------------------------------------------------------------------
-- Purpose: Saved as a View to find students who have submitted to Course ID = 1.
-- Demonstrates nested IN clauses.
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW StudentsInCourse AS
SELECT first_name, last_name 
FROM User 
WHERE user_id IN (
    SELECT student_id 
    FROM Submission 
    WHERE assignment_id IN (
        SELECT assignment_id 
        FROM Assignment 
        WHERE course_id = 1
    )
);

-- [EXAMPLE USAGE IN MYSQL TERMINAL]
-- Type this to see a list of students in Course #1:
-- SELECT * FROM StudentsInCourse;


-- ------------------------------------------------------------------------------
-- 5. AGGREGATE & SCALAR FUNCTIONS
-- ------------------------------------------------------------------------------
-- Purpose: Saved as a View to calculate overall system statistics.
-- Demonstrates COUNT(), AVG(), MAX(), and ROUND().
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW OverallSimilarityStats AS
SELECT 
    COUNT(similarity_id) as total_comparisons,
    ROUND(AVG(score), 4) AS avg_score, 
    MAX(score) AS max_score 
FROM Similarity;

-- [EXAMPLE USAGE IN MYSQL TERMINAL]
-- Type this to see total comparisons, average score, and highest score ever recorded:
-- SELECT * FROM OverallSimilarityStats;
