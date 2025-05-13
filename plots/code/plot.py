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


# --- Plot 1: Average Marks Per Subject ---
cursor.execute("""
    SELECT sub.subject_name, ROUND(AVG(m.marks), 2) AS avg_marks
    FROM marks m
    JOIN subjects sub ON m.subject_id = sub.subject_id
    GROUP BY m.subject_id;
""")
data = cursor.fetchall()
subjects = [row[0] for row in data]
avg_marks = [row[1] for row in data]

plt.figure(figsize=(6,4))
plt.bar(subjects, avg_marks, color='skyblue')
plt.title("Average Marks Per Subject")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.tight_layout()
plt.show()

# --- Plot 2: Attendance Percentage ---
cursor.execute("""
    SELECT s.name, 
           ROUND(SUM(CASE WHEN present = TRUE THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS attendance_pct
    FROM attendance a
    JOIN students s ON s.student_id = a.student_id
    GROUP BY a.student_id;
""")
data = cursor.fetchall()
names = [row[0] for row in data]
attendance = [row[1] for row in data]

plt.figure(figsize=(8,4))
plt.bar(names, attendance, color='lightgreen')
plt.title("Student Attendance Percentage")
plt.xticks(rotation=45)
plt.ylabel("Attendance %")
plt.tight_layout()
plt.show()

# Attendance Contribution per Student
cursor.execute("""
    SELECT s.name, 
           SUM(CASE WHEN present = TRUE THEN 1 ELSE 0 END) AS present_days
    FROM attendance a
    JOIN students s ON s.student_id = a.student_id
    GROUP BY s.student_id;
""")
data = cursor.fetchall()
names = [row[0] for row in data]
days_present = [row[1] for row in data]

plt.figure(figsize=(6,6))
plt.pie(days_present, labels=names, autopct='%1.1f%%', startangle=90)
plt.title("Attendance Distribution Among Students")
plt.tight_layout()
plt.show()


# Line Plot – Performance Trend for a Single Student
cursor.execute("""
    SELECT sub.subject_name, m.marks
    FROM marks m
    JOIN subjects sub ON m.subject_id = sub.subject_id
    WHERE m.student_id = 1;
""")
data = cursor.fetchall()
subjects = [row[0] for row in data]
marks = [row[1] for row in data]

plt.figure(figsize=(6,4))
plt.plot(subjects, marks, marker='o', linestyle='-', color='orange')
plt.title("Student 1 Performance Trend")
plt.xlabel("Subjects")
plt.ylabel("Marks")
plt.grid(True)
plt.tight_layout()
plt.show()

#Stacked Bar Chart – Subject-wise Top 3 Students

# Top 3 in Math
cursor.execute("""
    SELECT s.name, m.marks FROM marks m
    JOIN students s ON m.student_id = s.student_id
    WHERE subject_id = 101
    ORDER BY marks DESC LIMIT 3;
""")
math_data = cursor.fetchall()

# Top 3 in Physics
cursor.execute("""
    SELECT s.name, m.marks FROM marks m
    JOIN students s ON m.student_id = s.student_id
    WHERE subject_id = 102
    ORDER BY marks DESC LIMIT 3;
""")
physics_data = cursor.fetchall()

names = [row[0] for row in math_data]
math_scores = [row[1] for row in math_data]
physics_scores = [row[1] for row in physics_data]

bar_width = 0.35
x = range(len(names))

plt.figure(figsize=(8,5))
plt.bar(x, math_scores, width=bar_width, label='Math', color='blue')
plt.bar([p + bar_width for p in x], physics_scores, width=bar_width, label='Physics', color='green')

plt.xticks([p + bar_width/2 for p in x], names)
plt.title("Top 3 Students in Math vs Physics")
plt.ylabel("Marks")
plt.legend()
plt.tight_layout()
plt.show()

#Histogram – Distribution of All Marks
cursor.execute("SELECT marks FROM marks")
data = cursor.fetchall()
all_marks = [row[0] for row in data]

plt.figure(figsize=(6,4))
plt.hist(all_marks, bins=10, color='purple', edgecolor='black')
plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.show()


cursor.close()
conn.close()

