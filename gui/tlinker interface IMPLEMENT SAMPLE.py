import tkinter as tk
from tkinter import messagebox
import mysql.connector

def show_top_math_students():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Neels@trichy634",
            database="student_performance"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name, m.marks FROM marks m
            JOIN students s ON m.student_id = s.student_id
            WHERE m.subject_id = 101
            ORDER BY m.marks DESC LIMIT 3;
        """)
        rows = cursor.fetchall()
        result = "\n".join([f"{name}: {marks}" for name, marks in rows])
        messagebox.showinfo("Top 3 in Math", result)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Tkinter GUI
root = tk.Tk()
root.title("Student Performance Dashboard")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

title = tk.Label(frame, text="Student Performance Prediction", font=("Helvetica", 14, "bold"))
title.pack(pady=10)

btn = tk.Button(frame, text="Show Top 3 Math Students", command=show_top_math_students)
btn.pack(pady=10)

root.mainloop()
