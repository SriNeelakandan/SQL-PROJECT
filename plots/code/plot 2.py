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
SELECT s.name, SUM(m.marks) AS total_marks
FROM marks m
JOIN students s ON s.student_id = m.student_id
GROUP BY s.student_id;
""")
data = cursor.fetchall()
subjects = [row[0] for row in data]
total_marks = [row[1] for row in data]

plt.figure(figsize=(10,6))
plt.bar(subjects, total_marks, color='skyblue')
plt.title("Total Marks Per Student")
plt.xlabel("student")
plt.ylabel("total Marks")
plt.tight_layout()
plt.show()