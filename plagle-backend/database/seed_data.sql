-- PlagLe: Seed Data
-- Run this AFTER schema.sql to populate tables with sample data.

-- ============================================================
-- 1. Users (3 instructors, 1 admin, 10 students)
-- ============================================================
-- Passwords are bcrypt hashes of "Password@123"
INSERT INTO User (first_name, last_name, email, password_hash, role) VALUES
('Aarav',    'Sharma',    'aarav.sharma@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'admin'),
('Priya',    'Mehta',     'priya.mehta@plagle.edu',      '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'instructor'),
('Rajesh',   'Gupta',     'rajesh.gupta@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'instructor'),
('Neha',     'Iyer',      'neha.iyer@plagle.edu',        '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'instructor'),
('Rohan',    'Patel',     'rohan.patel@plagle.edu',      '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Ananya',   'Reddy',     'ananya.reddy@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Vikram',   'Singh',     'vikram.singh@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Sneha',    'Nair',      'sneha.nair@plagle.edu',       '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Aditya',   'Joshi',     'aditya.joshi@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Kavya',    'Deshmukh',  'kavya.deshmukh@plagle.edu',   '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Manish',   'Verma',     'manish.verma@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Diya',     'Chauhan',   'diya.chauhan@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Arjun',    'Kapoor',    'arjun.kapoor@plagle.edu',     '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student'),
('Ishita',   'Bose',      'ishita.bose@plagle.edu',      '$2b$12$LJ3m9Xz0QiVn0hF0vN2ZxOeBwWxKjG5Ht0gMpEyZ8v8DEFa6RiKC6', 'student');

-- ============================================================
-- 2. Courses (taught by the 3 instructors: user_id 2, 3, 4)
-- ============================================================
INSERT INTO Course (course_code, course_name, instructor_id) VALUES
('CS201',  'Data Structures and Algorithms',     2),
('CS301',  'Database Management Systems',         3),
('CS401',  'Machine Learning',                    4),
('CS102',  'Introduction to Programming',          2),
('CS350',  'Computer Networks',                    3);

-- ============================================================
-- 3. Assignments
-- ============================================================
INSERT INTO Assignment (course_id, title, description, due_date) VALUES
(1, 'Binary Search Tree Implementation',    'Implement a BST with insert, delete, and search operations in C++.',      '2026-04-20 23:59:00'),
(1, 'Graph Traversal Algorithms',           'Write BFS and DFS traversals for an adjacency-list graph.',               '2026-05-05 23:59:00'),
(2, 'ER Diagram Design',                    'Design an ER diagram for a library management system.',                   '2026-04-18 23:59:00'),
(2, 'SQL Query Optimization',               'Optimize the given set of slow-running queries using indexing.',           '2026-05-10 23:59:00'),
(3, 'Linear Regression from Scratch',       'Implement linear regression using only NumPy. No sklearn allowed.',       '2026-04-25 23:59:00'),
(3, 'Neural Network Backpropagation',       'Implement forward and backward pass for a 2-layer neural network.',       '2026-05-15 23:59:00'),
(4, 'Python Basics – String Manipulation',  'Solve the 5 string problems listed in the PDF.',                          '2026-04-22 23:59:00'),
(5, 'Socket Programming in C',             'Build a simple TCP client-server chat application.',                        '2026-04-28 23:59:00');

-- ============================================================
-- 4. Submissions (students: user_id 5–14)
-- ============================================================
INSERT INTO Submission (assignment_id, student_id, attempt_number) VALUES
-- Assignment 1 – BST (course CS201)
(1, 5,  1),   -- submission_id 1
(1, 6,  1),   -- submission_id 2
(1, 7,  1),   -- submission_id 3
(1, 8,  1),   -- submission_id 4
(1, 9,  1),   -- submission_id 5
(1, 10, 1),   -- submission_id 6
-- Assignment 2 – Graph Traversal
(2, 5,  1),   -- submission_id 7
(2, 6,  1),   -- submission_id 8
(2, 7,  1),   -- submission_id 9
(2, 11, 1),   -- submission_id 10
-- Assignment 3 – ER Diagram
(3, 8,  1),   -- submission_id 11
(3, 9,  1),   -- submission_id 12
(3, 10, 1),   -- submission_id 13
(3, 12, 1),   -- submission_id 14
-- Assignment 4 – SQL Optimization
(4, 5,  1),   -- submission_id 15
(4, 6,  1),   -- submission_id 16
(4, 13, 1),   -- submission_id 17
-- Assignment 5 – Linear Regression
(5, 7,  1),   -- submission_id 18
(5, 8,  1),   -- submission_id 19
(5, 14, 1),   -- submission_id 20
(5, 11, 1),   -- submission_id 21
-- Assignment 7 – Python Basics
(7, 5,  1),   -- submission_id 22
(7, 6,  1),   -- submission_id 23
(7, 12, 1),   -- submission_id 24
-- Assignment 8 – Socket Programming
(8, 9,  1),   -- submission_id 25
(8, 13, 1),   -- submission_id 26
(8, 14, 1),   -- submission_id 27
-- Re-submissions (attempt 2)
(1, 5,  2),   -- submission_id 28
(5, 7,  2);   -- submission_id 29

-- ============================================================
-- 5. Documents (one file per submission)
-- ============================================================
INSERT INTO Document (submission_id, file_name, file_path, file_hash) VALUES
(1,  'bst_rohan.cpp',           '/uploads/cs201/a1/bst_rohan.cpp',           'a3f1c9d8e7b24506f1a8c3e9d7b05142a6f8e3c1d9b74520f3a6c8e1d0b24537'),
(2,  'bst_ananya.cpp',          '/uploads/cs201/a1/bst_ananya.cpp',          'b4e2d0c9f8a35617e2b9d4f0c8a16253b7e9f4d2c0a85631e4b7d9f2c1a35648'),
(3,  'bst_vikram.cpp',          '/uploads/cs201/a1/bst_vikram.cpp',          'c5f3e1d0a9b46728f3c0e5a1d9b27364c8f0a5e3d1b96742f5c8e0a3d2b46759'),
(4,  'bst_sneha.cpp',           '/uploads/cs201/a1/bst_sneha.cpp',           'd6a4f2e1b0c57839a4d1f6b2e0c38475d9a1b6f4e2c07853a6d9f1b4e3c57860'),
(5,  'bst_aditya.cpp',          '/uploads/cs201/a1/bst_aditya.cpp',          'e7b5a3f2c1d68940b5e2a7c3f1d49586e0b2c7a5f3d18964b7e0a2c5f4d68971'),
(6,  'bst_kavya.cpp',           '/uploads/cs201/a1/bst_kavya.cpp',           'f8c6b4a3d2e79051c6f3b8d4a2e50697f1c3d8b6a4e29075c8f1b3d6a5e79082'),
(7,  'graph_rohan.cpp',         '/uploads/cs201/a2/graph_rohan.cpp',         '19d7c5b4e3f80162d7a4c9e5b3f61708a2d4e9c7b5f30186d9a2c4e7b6f80193'),
(8,  'graph_ananya.cpp',        '/uploads/cs201/a2/graph_ananya.cpp',        '20e8d6c5f4a91273e8b5d0f6c4a72819b3e5f0d8c6a41297e0b3d5f8c7a91204'),
(9,  'graph_vikram.cpp',        '/uploads/cs201/a2/graph_vikram.cpp',        '31f9e7d6a5b02384f9c6e1a7d5b83920c4f6a1e9d7b52308f1c4e6a9d8b02315'),
(10, 'graph_manish.cpp',        '/uploads/cs201/a2/graph_manish.cpp',        '42a0f8e7b6c13495a0d7f2b8e6c94031d5a7b2f0e8c63419a2d5f7b0e9c13426'),
(11, 'er_sneha.pdf',            '/uploads/cs301/a3/er_sneha.pdf',            '53b1a9f8c7d24506b1e8a3c9f7d05142e6b8c3a1f9d74530b3e6a8c1f0d24537'),
(12, 'er_aditya.pdf',           '/uploads/cs301/a3/er_aditya.pdf',           '64c2b0a9d8e35617c2f9b4d0a8e16253f7c9d4b2a0e85641c4f7b9d2a1e35648'),
(13, 'er_kavya.pdf',            '/uploads/cs301/a3/er_kavya.pdf',            '75d3c1b0e9f46728d3a0c5e1b9f27364a8d0e5c3b1f96752d5a8c0e3b2f46759'),
(14, 'er_diya.pdf',             '/uploads/cs301/a3/er_diya.pdf',             '86e4d2c1f0a57839e4b1d6f2c0a38475b9e1f6d4c2a07863e6b9d1f4c3a57860'),
(15, 'sql_rohan.sql',           '/uploads/cs301/a4/sql_rohan.sql',           '97f5e3d2a1b68940f5c2e7a3d1b49586c0f2a7e5d3b18974f7c0e2a5d4b68971'),
(16, 'sql_ananya.sql',          '/uploads/cs301/a4/sql_ananya.sql',          '08a6f4e3b2c79051a6d3f8b4e2c50697d1a3b8f6e4c29085a8d1f3b6e5c79082'),
(17, 'sql_arjun.sql',           '/uploads/cs301/a4/sql_arjun.sql',           '19b7a5f4c3d80162b7e4a9c5f3d61708e2b4c9a7f5d30196b9e2a4c7f6d80193'),
(18, 'linreg_vikram.py',        '/uploads/cs401/a5/linreg_vikram.py',        '20c8b6a5d4e91273c8f5b0d6a4e72819f3c5d0b8a6e41207c0f3b5d8a7e91204'),
(19, 'linreg_sneha.py',         '/uploads/cs401/a5/linreg_sneha.py',         '31d9c7b6e5f02384d9a6c1e7b5f83920a4d6e1c9b7f52318d1a4c6e9b8f02315'),
(20, 'linreg_ishita.py',        '/uploads/cs401/a5/linreg_ishita.py',        '42e0d8c7f6a13495e0b7d2f8c6a94031b5e7f2d0c8a63429e2b5d7f0c9a13426'),
(21, 'linreg_manish.py',        '/uploads/cs401/a5/linreg_manish.py',        '53f1e9d8a7b24506f1c8e3a9d7b05142c6f8a3e1d9b74540f3c6e8a1d0b24537'),
(22, 'strings_rohan.py',        '/uploads/cs102/a7/strings_rohan.py',        '64a2f0e9b8c35617a2d9f4b0e8c16253d7a9b4f2e0c85651a4d7f9b2e1c35648'),
(23, 'strings_ananya.py',       '/uploads/cs102/a7/strings_ananya.py',       '75b3a1f0c9d46728b3e0a5c1f9d27364e8b0c5a3f1d96762b5e8a0c3f2d46759'),
(24, 'strings_diya.py',         '/uploads/cs102/a7/strings_diya.py',         '86c4b2a1d0e57839c4f1b6d2a0e38475f9c1d6b4a2e07873c6f9b1d4a3e57860'),
(25, 'socket_aditya.c',         '/uploads/cs350/a8/socket_aditya.c',         '97d5c3b2e1f68940d5a2c7e3b1f49586a0d2e7c5b3f18984d7a0c2e5b4f68971'),
(26, 'socket_arjun.c',          '/uploads/cs350/a8/socket_arjun.c',          '08e6d4c3f2a79051e6b3d8f4c2a50697b1e3f8d6c4a29095e8b1d3f6c5a79082'),
(27, 'socket_ishita.c',         '/uploads/cs350/a8/socket_ishita.c',         '19f7e5d4a3b80162f7c4e9a5d3b61708c2f4a9e7d5b30106f9c2e4a7d6b80193'),
-- Re-submission documents
(28, 'bst_rohan_v2.cpp',        '/uploads/cs201/a1/bst_rohan_v2.cpp',        'aa11b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f001'),
(29, 'linreg_vikram_v2.py',     '/uploads/cs401/a5/linreg_vikram_v2.py',     'bb22c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f002');

-- ============================================================
-- 6. Algorithms
-- ============================================================
INSERT INTO Algorithm (name, version, description) VALUES
('TF-IDF Cosine',      '1.0',  'Term Frequency–Inverse Document Frequency with cosine similarity measurement.'),
('Jaccard Index',      '1.0',  'Set-based similarity using intersection over union of token sets.'),
('Winnowing',          '2.1',  'Local fingerprinting algorithm for document similarity (Schleimer et al.).'),
('Levenshtein Ratio',  '1.0',  'Normalized edit-distance based similarity between two strings.'),
('AST Comparison',     '1.0',  'Abstract Syntax Tree structural comparison for source code similarity.');

-- ============================================================
-- 7. Similarity results
--    score is DECIMAL(5,4) so values are between 0.0000 and 1.0000
--    doc1_id < doc2_id is enforced by CHECK constraint
-- ============================================================
INSERT INTO Similarity (doc1_id, doc2_id, algorithm_id, score) VALUES
-- BST submissions – high similarity pair (Rohan & Ananya) → potential plagiarism
(1,  2,  1, 0.9210),   -- TF-IDF Cosine
(1,  2,  3, 0.8845),   -- Winnowing
(1,  2,  5, 0.9102),   -- AST Comparison
-- BST submissions – moderate similarity
(1,  3,  1, 0.4520),
(2,  3,  1, 0.4310),
(3,  4,  1, 0.3870),
(4,  5,  1, 0.3150),
(5,  6,  1, 0.2980),
-- BST – re-submission vs originals
(2,  28, 1, 0.6110),   -- Rohan v2 vs Ananya
(2,  28, 5, 0.5530),   -- AST of same pair
-- Graph traversal – another suspicious pair (Rohan & Ananya again)
(7,  8,  1, 0.8750),
(7,  8,  3, 0.8620),
(7,  9,  1, 0.3200),
(8,  10, 1, 0.2910),
-- ER Diagram
(11, 12, 2, 0.5600),   -- Jaccard
(12, 13, 2, 0.4100),
(13, 14, 2, 0.3800),
-- SQL Optimization – high similarity (Rohan & Ananya copying pattern)
(15, 16, 1, 0.9450),
(15, 16, 4, 0.9120),   -- Levenshtein
(15, 17, 1, 0.3050),
-- Linear Regression
(18, 19, 1, 0.7800),   -- moderate-high
(18, 19, 5, 0.7200),   -- AST
(19, 20, 1, 0.3600),
(20, 21, 1, 0.2750),
-- Python Strings – high similarity (Rohan & Ananya once more)
(22, 23, 1, 0.9670),
(22, 23, 4, 0.9510),
(23, 24, 1, 0.4200),
-- Socket Programming
(25, 26, 1, 0.5100),
(25, 27, 1, 0.4850),
(26, 27, 1, 0.3300);

-- ============================================================
-- 8. Reports (generated by instructors)
-- ============================================================
INSERT INTO Report (similarity_id, generated_by, summary_notes, report_pdf_path) VALUES
(1,  2, 'CRITICAL: Rohan Patel and Ananya Reddy BST submissions show 92.1% TF-IDF similarity. Variable names differ but logic and structure are nearly identical. Recommend academic integrity review.',
        '/reports/cs201_a1_rohan_ananya_tfidf.pdf'),
(3,  2, 'AST comparison confirms structural plagiarism between Rohan and Ananya BST code (91.02%). Combined with TF-IDF result, strong evidence of copying.',
        '/reports/cs201_a1_rohan_ananya_ast.pdf'),
(11, 2, 'Graph traversal submissions of Rohan and Ananya again show high similarity (87.5%). Repeat offence pattern detected across assignments.',
        '/reports/cs201_a2_rohan_ananya_tfidf.pdf'),
(18, 3, 'SQL query optimization: Rohan and Ananya submissions 94.5% similar. Near-identical query rewrites including same aliasing conventions.',
        '/reports/cs301_a4_rohan_ananya_tfidf.pdf'),
(21, 4, 'Linear regression: Vikram and Sneha show 78% TF-IDF similarity. Code structure differs somewhat; may be coincidental due to assignment constraints. Further review recommended.',
        '/reports/cs401_a5_vikram_sneha_tfidf.pdf'),
(25, 2, 'Python strings: Rohan and Ananya at 96.7% similarity. Fourth flagged instance across courses. Escalating to department head.',
        '/reports/cs102_a7_rohan_ananya_tfidf.pdf');
