import sqlite3
import subprocess
import tkinter as tk

from tkinter import *
from tkinter import ttk
from tkinter import messagebox



# Create the Main Window
root = Tk()
root.title("Courses Information Management V2.0")
root.geometry("600x410")
root.resizable(False, False)
course_list = ttk.Treeview(root)

conn = sqlite3.connect("version2.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    coursecode TEXT,
                    coursename TEXT)''')



# Function to fetch and display courses
def rtv():
    # Clear the tree view
    course_list.delete(*course_list.get_children())

    # Fetch courses from the database
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()

    # Insert courses into the tree view
    for idx, row in enumerate(rows):
        course_list.insert(parent="", index=idx, iid=idx, text=row[0], values=(row[1], row[2]))


# Function to add a course
def add_course():
    coursecode = coursecode_entry.get() or "-"
    coursename = coursename_entry.get() or "-"

    # Add course to the database
    cursor.execute(
        "INSERT INTO courses (coursecode, coursename) VALUES (?, ?)",
        (coursecode, coursename))
    conn.commit()

    # Clear entry fields and refresh the tree view
    coursecode_entry.delete(0, tk.END)
    coursename_entry.delete(0, tk.END)

    rtv()


# Function to delete a course
def delete_course():
    # Get the selected item from the tree view
    selected_item = course_list.selection()
    if not selected_item:
        return

    # Get the course code of the selected course
    course_code = course_list.item(selected_item)["values"][0]

    # Check if the course code is used in the students table
    cursor.execute("SELECT * FROM students WHERE course = ?", (course_code,))
    students = cursor.fetchall()

    if len(students) > 0:
        # Display an error message using a dialogue prompt
        messagebox.showerror("Error Deleting", "The selected course has students enrolled. Remove or update students from this course to proceed.")
        return

    # Get the ID of the selected course
    item_id = course_list.item(selected_item)["text"]

    # Ask for confirmation using a dialogue prompt
    confirm = messagebox.askyesno("Hold up.", "Are you absolutely sure you want to delete this course?")

    if confirm:
        # Delete the course from the database using ID
        cursor.execute("DELETE FROM courses WHERE id=?", (item_id,))
        conn.commit()

        # Delete the selected course from the tree view
        course_list.delete(selected_item)

        rtv()


# Function to update a course
def update_course():
    # Get the selected item from the tree view
    selected_item = course_list.selection()
    if not selected_item:
        return

    # Get the ID of the selected course
    item_id = course_list.item(selected_item)["text"]

    # Get the current values of the selected course
    current_values = course_list.item(selected_item)["values"]

    # Get the updated values from the entry fields
    coursecode = coursecode_entry.get() or current_values[0]
    coursename = coursename_entry.get() or current_values[1]

    # Update the course data in the database
    cursor.execute(
        "UPDATE courses SET coursecode=?, coursename=? WHERE id=?",
        (coursecode, coursename, item_id))
    conn.commit()

    # Clear entry fields and refresh the tree view
    coursecode_entry.delete(0, tk.END)
    coursename_entry.delete(0, tk.END)

    rtv()


# Function to OPEN SSISv2.py
def open_program():
    program_path = "D:/Downloads/SSIS/ssis(2).py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")

    root.destroy()


# Function to SEARCH
def search():
    search_text = search_entry.get()

    # Clear the tree view
    course_list.delete(*course_list.get_children())

    # Fetch courses from the database
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()

    # Insert matching courses into the tree view
    for idx, row in enumerate(rows):
        values = (row[1], row[2])
        found = False

        # Check
        for value in values:
            if search_text.lower() in str(value).lower():
                found = True
                break

        # Insert
        if found:
            course_list.insert(parent="", index=idx, iid=idx, text=row[0], values=values)

    # Clear
    search_entry.delete(0, tk.END)



# Buttons
add_button = tk.Button(root, text="Add Course", command=add_course, bg="#abdbe3")
add_button.grid(row=2, column=1, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Course", command=delete_course, bg="#F77070")
delete_button.grid(row=5, column=0, padx=5, pady=5)

update_button = tk.Button(root, text="Update", command=update_course)
update_button.grid(row=2, column=0, padx=5, pady=5)

ssis_button = tk.Button(root, text="Students", command=open_program, bg="#eab676")
ssis_button.grid(row=5, column=1, padx=5, pady=5)

search_button = tk.Button(root, text="Search", command=search)
search_button.grid(row=3, column=1, padx=5, pady=5)



# Course Information Form
coursecode_label = tk.Label(root, text="Course Code:")
coursecode_label.grid(row=0, column=0, padx=5, pady=5)
coursecode_entry = tk.Entry(root)
coursecode_entry.grid(row=0, column=1, padx=5, pady=5)

coursename_label = tk.Label(root, text="Course Name:")
coursename_label.grid(row=1, column=0, padx=5, pady=5)
coursename_entry = tk.Entry(root)
coursename_entry.grid(row=1, column=1, padx=5, pady=5)

search_entry = tk.Entry(root)
search_entry.grid(row=3, column=0, padx=5, pady=5)



# Treeview
course_list = ttk.Treeview(root)
course_list["columns"] = ("coursecode", "coursename")
course_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

course_list.heading("#0", text="ID")
course_list.heading("coursecode", text="Course Code")
course_list.heading("coursename", text="Course")

course_list.column("#0", width=0, stretch=tk.NO)
course_list.column("coursecode", width=150, anchor=tk.CENTER)
course_list.column("coursename", width=440, anchor=tk.CENTER)



rtv()
root.mainloop()
