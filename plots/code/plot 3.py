import mysql.connector
import matplotlib.pyplot as plt

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Neels@trichy634",
    database="student_performance"
)
cursor = conn.cursor()

#PLOT 1. List of all students with total marks
cursor.execute("""
SELECT DISTINCT s.name, sub.subject_name, m.marks
FROM marks m
JOIN students s ON s.student_id = m.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
WHERE m.marks >= 90;
""")
data = cursor.fetchall()
labels = [f"{row[0]} - {row[1]}" for row in data]  # e.g., "Alice - Math"
marks = [row[2] for row in data]

plt.figure(figsize=(10,6))
plt.bar(labels, marks, color='lightgreen')
plt.title("Students Scoring ≥ 90 in Subjects")
plt.xlabel("Marks")
plt.tight_layout()
plt.show()


