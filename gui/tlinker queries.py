import tkinter as tk
from tkinter import messagebox
import mysql.connector

def run_query(query, headers, title):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Neels@trichy634",
            database="student_performance"
        )
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        result = "\n".join([", ".join(map(str, row)) for row in data])
        if not result:
            result = "No data found."
        messagebox.showinfo(title, f"{headers}\n\n{result}")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# 10 queries as button callbacks
def query1():  # Top 3 in Math
    run_query(
        """
        SELECT s.name, m.marks FROM marks m
        JOIN students s ON s.student_id = m.student_id
        WHERE m.subject_id = 101
        ORDER BY m.marks DESC LIMIT 3;
        """,
        "Name, Math Marks",
        "Top 3 in Math"
    )

def query2():  # Average marks per subject
    run_query(
        """
        SELECT sub.subject_name, ROUND(AVG(m.marks), 2)
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.subject_id
        GROUP BY m.subject_id;
        """,
        "Subject, Avg Marks",
        "Average Marks per Subject"
    )

def query3():  # Low attendance
    run_query(
        """
        SELECT s.name, 
        ROUND(SUM(CASE WHEN present = TRUE THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS attendance_pct
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        GROUP BY a.student_id
        HAVING attendance_pct < 75;
        """,
        "Name, Attendance %",
        "Students with Low Attendance"
    )

def query4():  # Total students per class
    run_query(
        """
        SELECT class, COUNT(*) FROM students GROUP BY class;
        """,
        "Class, Total Students",
        "Students per Class"
    )

def query5():  # Best performing student overall
    run_query(
        """
        SELECT s.name, ROUND(AVG(m.marks), 2) as avg_marks
        FROM marks m
        JOIN students s ON s.student_id = m.student_id
        GROUP BY m.student_id
        ORDER BY avg_marks DESC LIMIT 1;
        """,
        "Name, Average Marks",
        "Top Overall Performer"
    )

def query6():  # Students failing in any subject (< 35)
    run_query(
        """
        SELECT s.name, sub.subject_name, m.marks
        FROM marks m
        JOIN students s ON s.student_id = m.student_id
        JOIN subjects sub ON m.subject_id = sub.subject_id
        WHERE m.marks < 35;
        """,
        "Name, Subject, Marks",
        "Failing Students (<35)"
    )

def query7():  # Highest marks in each subject
    run_query(
        """
        SELECT sub.subject_name, MAX(m.marks)
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.subject_id
        GROUP BY m.subject_id;
        """,
        "Subject, Max Marks",
        "Top Scores in Each Subject"
    )

def query8():  # Attendance percentage for each student
    run_query(
        """
        SELECT s.name, 
        ROUND(SUM(CASE WHEN present = TRUE THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS attendance_pct
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        GROUP BY a.student_id;
        """,
        "Name, Attendance %",
        "Attendance Percentage"
    )

def query9():  # Student list sorted by average marks
    run_query(
        """
        SELECT s.name, ROUND(AVG(m.marks), 2) as avg_marks
        FROM marks m
        JOIN students s ON s.student_id = m.student_id
        GROUP BY m.student_id
        ORDER BY avg_marks DESC;
        """,
        "Name, Avg Marks",
        "Students Sorted by Avg Marks"
    )

def query10():  # Subject-wise student count
    run_query(
        """
        SELECT sub.subject_name, COUNT(DISTINCT m.student_id)
        FROM marks m
        JOIN subjects sub ON m.subject_id = sub.subject_id
        GROUP BY m.subject_id;
        """,
        "Subject, No. of Students",
        "Students per Subject"
    )

# GUI layout
root = tk.Tk()
root.title("Student Performance Dashboard")
root.geometry("400x550")

tk.Label(root, text="Student Performance Analyzer", font=("Arial", 14, "bold"), pady=10).pack()

buttons = [
    ("Top 3 in Math", query1),
    ("Average Marks per Subject", query2),
    ("Low Attendance (<75%)", query3),
    ("Total Students per Class", query4),
    ("Top Overall Performer", query5),
    ("Failing Students (<35)", query6),
    ("Highest Marks per Subject", query7),
    ("Attendance % of Students", query8),
    ("Students by Avg Marks", query9),
    ("Students per Subject", query10),
]

for text, cmd in buttons:
    tk.Button(root, text=text, width=35, command=cmd, pady=5).pack(pady=5)

root.mainloop()
