USE student_performance;

-- 1. Average marks per subject
SELECT subject_id, AVG(marks) AS avg_marks FROM marks GROUP BY subject_id;


-- 2. Top 3 performers in Math
SELECT s.name, m.marks FROM marks m
JOIN students s ON m.student_id = s.student_id
WHERE m.subject_id = 102
ORDER BY m.marks DESC
LIMIT 3;

-- 3. Subject-wise highest mark
SELECT subject_id, MAX(marks) AS max_marks FROM marks GROUP BY subject_id;

-- 4. Students with any mark < 50 (low performers)
SELECT DISTINCT s.name FROM marks m
JOIN students s ON m.student_id = s.student_id
WHERE m.marks < 50;

SELECT * FROM students;
-- 5. Attendance percentage of each student
SELECT a.student_id, 
       ROUND(SUM(CASE WHEN present = TRUE THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS attendance_pct
FROM attendance a
GROUP BY a.student_id;

-- 6. Students with attendance < 75%
SELECT s.name, ROUND(SUM(CASE WHEN present = TRUE THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS attendance_pct
FROM attendance a
JOIN students s ON s.student_id = a.student_id
GROUP BY a.student_id
HAVING attendance_pct < 75;

-- 7. Students with average marks > 80
SELECT s.name, ROUND(AVG(m.marks), 2) AS avg_marks
FROM marks m
JOIN students s ON s.student_id = m.student_id
GROUP BY m.student_id
HAVING avg_marks > 80;

-- 8. List of all students with total marks
SELECT s.name, SUM(m.marks) AS total_marks
FROM marks m
JOIN students s ON s.student_id = m.student_id
GROUP BY s.student_id;

-- 9. Subject-wise average mark with subject names
SELECT sub.subject_name, ROUND(AVG(m.marks), 2) AS avg_marks
FROM marks m
JOIN subjects sub ON m.subject_id = sub.subject_id
GROUP BY m.subject_id;
SELECT * FROM  marks;
-- 10. Students who scored 90 or above in any subject
SELECT DISTINCT s.name, m.marks
FROM marks m
JOIN students s ON s.student_id = m.student_id
WHERE m.marks >= 90;

SELECT DISTINCT s.name, sub.subject_name, m.marks
FROM marks m
JOIN students s ON s.student_id = m.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
WHERE m.marks >= 90;
