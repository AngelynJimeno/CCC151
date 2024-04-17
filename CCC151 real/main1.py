import tkinter as tk
from tkinter import ttk
import csv
import tkinter.messagebox as messagebox
import re
#============================#

#Adding student to the csv
def add_student():
    id_number = IDno_ent.get()
    last_name = name_ent.get()
    first_name = name1_ent.get()  
    middle_name = name2_ent.get()  
    yearlvl = Yearlvl_ent.get()
    gender = gender_ent.get()
    course_code = Coursecd_ent.get()

    if id_number and last_name and first_name and middle_name and yearlvl and gender and course_code:
        # Validate ID number format
        if not re.match(r'^\d{4}-\d{4}$', id_number):
            messagebox.showerror("Invalid ID Number Format", "ID number must be in the format '0000-0000'.")
            return

    if id_number and last_name and first_name and middle_name and yearlvl and gender and course_code:
        if course_code not in course_codes:
            messagebox.showerror("Course Not Found", f"The course code '{course_code}' was not found.")
            return
        
        with open('students.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == id_number:
                    messagebox.showerror("ID Number Already Exists", f"The ID number '{id_number}' already exists.")
                    return
        
        with open('students.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([id_number, last_name, first_name, middle_name, yearlvl, gender, course_code])  

        clear_entries()
        update_student_table()

    else:
        messagebox.showerror("Missing Information", "Please fill in all fields.")

#Removing a student record
def delete_student():
    selected_item = student_table.selection()
    if selected_item:
        for item in selected_item:
            student_table.delete(item)
        update_student_csv()

#========================#
def update_student():
    selected_item = student_table.selection()
    if selected_item:
        for item in selected_item:
            student_id = student_table.item(item, 'values')[0]
            update_student_window(student_id)

def update_student_window(student_id):
    with open('students.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == student_id: 
                IDno_ent.delete(0, tk.END)
                IDno_ent.insert(0, row[0])  
                name_ent.delete(0, tk.END)
                name_ent.insert(0, row[1])
                name1_ent.delete(0, tk.END)  
                name1_ent.insert(0, row[2])  
                name2_ent.delete(0, tk.END)  
                name2_ent.insert(0, row[3])  
                Yearlvl_ent.set(row[4])  
                gender_ent.set(row[5])  
                Coursecd_ent.delete(0, tk.END)
                Coursecd_ent.insert(0, row[6])  
                break

def update_student_table():
    student_table.delete(*student_table.get_children())  
    
    try:
        with open('students.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                if row[6] in course_codes:
                    student_table.insert('', tk.END, values=row)
    except FileNotFoundError:
        print("CSV file not found.")
    except IndexError:
        print("Index out of range.")

def update_student_csv():
    with open('students.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID Number", "Last Name", "First Name", "Middle Name", "Year Level", "Gender", "Course"])  
        for row in student_table.get_children():
            values = student_table.item(row, 'values')
            writer.writerow(values)
#==========================#

def clear_entries():
    IDno_ent.delete(0, tk.END)
    name_ent.delete(0, tk.END)
    name1_ent.delete(0, tk.END)  
    name2_ent.delete(0, tk.END)  
    Yearlvl_ent.set('')
    gender_ent.set('')
    Coursecd_ent.delete(0, tk.END)

def on_student_select(event):
    selected_item = student_table.selection()
    if selected_item:
        selected_id = student_table.item(selected_item)['values'][0]  
        print("Selected student ID:", selected_id)

course_codes = []

new_csv_filename = 'students.csv' 
courses_csv_filename = 'courses.csv'

def load_course_codes():
    global course_codes
    course_codes = []  # Clear the existing course codes list
    try:
        with open(courses_csv_filename, 'r') as file:
            reader = csv.reader(file)
            for row_number, row in enumerate(reader, start=1):
                try:
                    if row:  # Check if the row is not empty
                        course_codes.append(row[0])  # Append the course code to the list
                except IndexError:
                    print(f"Error loading course code from row {row_number}: {row}")
    except FileNotFoundError:
        print("Courses CSV file not found.")
    except Exception as e:
        print("Error loading course codes:", e)

load_course_codes()

def save_course():
    course_code = addCoursecd_ent.get()
    if course_code:
        try:
            with open('courses.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                # Check if the course code already exists
                if course_code in course_codes:
                    messagebox.showinfo("Course Exists", f"The course '{course_code}' already exists.")
                else:
                    writer.writerow([course_code])
                    messagebox.showinfo("Course Added", f"The course '{course_code}' was added successfully!")

            load_course_codes()

            # Clear entry fields after adding course
            addCoursecd_ent.delete(0, tk.END)
            addCoursecd_ent.insert(0, "Enter Course Code")
            addCoursetitle_ent.delete(0, tk.END)
            addCoursetitle_ent.insert(0, "Enter Course Title")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving course: {e}")
    else:
        messagebox.showerror("Error", "Please enter a course code.")

#delete course
def delete_course():
    course_code = delCoursecd_ent.get()
    print("Course code to delete:", course_code)  
    if course_code:
        try:
            with open('courses.csv', 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)
                print("Original rows:", rows)  
            with open('courses.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                for row in rows:
                    if row[0] != course_code:
                        writer.writerow(row)
                print("New rows:", rows)  
            
            load_course_codes()
            
            delCoursecd_ent.delete(0, tk.END)  
            delCoursecd_ent.insert(0, "Enter Course Code")  
            delCoursetitle_ent.delete(0, tk.END)  
            delCoursetitle_ent.insert(0, "Enter Course Title")  
        except Exception as e:
            print("Error deleting course:", e)

#searching student using ID No
def search_student():
    search_id = search_ent.get()  
    if search_id:
        found = False
        for row in student_table.get_children():
            values = student_table.item(row, 'values')
            if values[0] == search_id:  
                student_table.selection_set(row)  #This will select the row if found
                student_table.focus(row)  
                found = True
                break
        if not found:
            messagebox.showinfo("Search", f"No student found with ID number: {search_id}")
    else:
        messagebox.showinfo("Search", "Please enter an ID number to search for.")

def refresh_table():
    load_course_codes()
    update_student_table()
#============================#
#=======GUI==========#
win = tk.Tk()
win.geometry("800x580+360+130")
win.title("Student Information System")

title_label = tk.Label(win, text="Student Information System", font=("Arial", 30, "bold"), border=8, relief=tk.GROOVE,bg="#455a64", foreground="#90a4ae")
title_label.pack(side=tk.TOP, fill=tk.X)

detail_frame = tk.LabelFrame(win, text="Student Details", font=("Arial", 17, "bold"), bg="#455a64", fg="#90a4ae", bd=5,relief=tk.GROOVE)
detail_frame.place(x=20, y=90, width=260, height=466)

data_frame = tk.Frame(win, bg="#455864", bd=5, relief=tk.GROOVE)
data_frame.place(x=300, y=90, width=477, height=350)

addcourse_frame = tk.LabelFrame(win, text="Add Course", font=("Arial", 14, "bold"), bg="#455a64", fg="#90a4ae", bd=5,relief=tk.GROOVE)
addcourse_frame.place(x=300, y=450, width=230, height=107)

deletecourse_frame = tk.LabelFrame(win, text="Delete Course", font=("Arial", 14, "bold"), bg="#455a64", fg="#90a4ae", bd=5,relief=tk.GROOVE)
deletecourse_frame.place(x=546, y=450, width=230, height=107)

# ==== ENTRY ====#
IDno_lbl = tk.Label(detail_frame, text="ID Number", font=('Arial', 9, "bold"), bg="#455864")
IDno_lbl.grid(row=0, column=0, padx=2, pady=2)

IDno_ent = tk.Entry(detail_frame, bd=7, font=('Arial', 9))
IDno_ent.grid(row=0, column=1, padx=2, pady=2)

name_lbl = tk.Label(detail_frame, text="Last Name", font=('Arial', 9, "bold"), bg="#455864")
name_lbl.grid(row=1, column=0, padx=2, pady=2)

name_ent = tk.Entry(detail_frame, bd=7, font=('Arial', 9))
name_ent.grid(row=1, column=1, padx=2, pady=2)

name1_lbl = tk.Label(detail_frame, text="First Name", font=('Arial', 9, "bold"), bg="#455864")
name1_lbl.grid(row=2, column=0, padx=2, pady=2)

name1_ent = tk.Entry(detail_frame, bd=7, font=('Arial', 9))
name1_ent.grid(row=2, column=1, padx=2, pady=2)

name2_lbl = tk.Label(detail_frame, text="Middle Name", font=('Arial', 9, "bold"), bg="#455864")
name2_lbl.grid(row=3, column=0, padx=2, pady=2)

name2_ent = tk.Entry(detail_frame, bd=7, font=('Arial', 9))
name2_ent.grid(row=3, column=1, padx=2, pady=2)


Yearlvl_lbl = tk.Label(detail_frame, text="Year Level", font=('Arial', 9, "bold"), bg="#455864")
Yearlvl_lbl.grid(row=4, column=0, padx=2, pady=2)

Yearlvl_ent = ttk.Combobox(detail_frame, text="Year Level", font=('Arial', 9), state="readonly")
Yearlvl_ent.grid(row=4, column=1, padx=2, pady=2)
Yearlvl_ent['values'] = ("1st Year", "2nd Year", "3rd Year", "4th Year")

gender_lbl = tk.Label(detail_frame, text="Gender", font=('Arial', 9, "bold"), bg="#455864")
gender_lbl.grid(row=5, column=0, padx=2, pady=2)

gender_ent = ttk.Combobox(detail_frame, text="Gender", font=('Arial', 9), state="readonly")
gender_ent.grid(row=5, column=1, padx=2, pady=2)
gender_ent['values'] = ("Male", "Female", "Other")

Coursecd_lbl = tk.Label(detail_frame, text="Course Code", font=('Arial', 9, "bold"), bg="#455864")
Coursecd_lbl.grid(row=6, column=0, padx=2, pady=2)

Coursecd_ent = ttk.Combobox(detail_frame, text="Course Code", font=('Arial', 9))
Coursecd_ent.grid(row=6, column=1, padx=2, pady=2)
Coursecd_ent['values'] = course_codes


addCoursecd_ent = tk.Entry(addcourse_frame, bd=7, font=('Arial', 9))
addCoursecd_ent.grid(row=0, column=0, columnspan=2, padx=2, pady=2)
addCoursecd_ent.insert(0, "Enter Course Code")  # Initial message

def on_add_course_focus_in(event):
    if addCoursecd_ent.get() == "Enter Course Code":
        addCoursecd_ent.delete(0, tk.END)

addCoursecd_ent.bind("<FocusIn>", on_add_course_focus_in)

addCoursetitle_ent = tk.Entry(addcourse_frame, bd=7, font=('Arial', 9))
addCoursetitle_ent.grid(row=1, column=0, columnspan=2, padx=2, pady=2)
addCoursetitle_ent.insert(0, "Enter Course Title")  # Initial message

def on_add_title_focus_in(event):
    if addCoursetitle_ent.get() == "Enter Course Title":
        addCoursetitle_ent.delete(0, tk.END)

addCoursetitle_ent.bind("<FocusIn>", on_add_title_focus_in)

save_btn = tk.Button(addcourse_frame, bg="#455864", text="Save", bd=5, font=("Arial", 8, "bold"), width=6)
save_btn.grid(row=0, column=3, padx=2, pady=2)
save_btn.config(command=save_course)


delCoursecd_ent = tk.Entry(deletecourse_frame, bd=7, font=('Arial', 9))
delCoursecd_ent.grid(row=0, column=0, columnspan=2, padx=2, pady=2)
delCoursecd_ent.insert(0, "Enter Course Code")  # Initial message

def on_del_course_focus_in(event):
    if delCoursecd_ent.get() == "Enter Course Code":
        delCoursecd_ent.delete(0, tk.END)

delCoursecd_ent.bind("<FocusIn>", on_del_course_focus_in)

delCoursetitle_ent = tk.Entry(deletecourse_frame, bd=7, font=('Arial', 9))
delCoursetitle_ent.grid(row=1, column=0, columnspan=2, padx=2, pady=2)
delCoursetitle_ent.insert(0, "Enter Course Title")  # Initial message

def on_del_title_focus_in(event):
    if delCoursetitle_ent.get() == "Enter Course Title":
        delCoursetitle_ent.delete(0, tk.END)

delCoursetitle_ent.bind("<FocusIn>", on_del_title_focus_in)

del_btn = tk.Button(deletecourse_frame, bg="#455864", text="Save", bd=5, font=("Arial", 8, "bold"), width=6)
del_btn.grid(row=0, column=3, padx=2, pady=2)
del_btn.config(command=delete_course)
# ===============#
# ====Buttons====#
btn_frame = tk.Frame(detail_frame, bg="#455864", bd=5, relief=tk.GROOVE)
btn_frame.place(x=8, y=380, width=237, height=45)  

add_btn = tk.Button(btn_frame, bg="#455864", text="Add", bd=5, font=("Arial", 8), width=6)
add_btn.grid(row=0, column=0, padx=2, pady=2)
add_btn.config(command=add_student)

update_btn = tk.Button(btn_frame, bg="#455864", text="Update", bd=5, font=("Arial", 8), width=6)
update_btn.grid(row=0, column=1, padx=3, pady=2)
update_btn.config(command=update_student)

delete_btn = tk.Button(btn_frame, bg="#455864", text="Delete", bd=5, font=("Arial", 8), width=6)
delete_btn.grid(row=0, column=2, padx=2, pady=2)
delete_btn.config(command=delete_student)

clear_btn = tk.Button(btn_frame, bg="#455864", text="Clear", bd=5, font=("Arial", 8), width=6)
clear_btn.grid(row=0, column=3, padx=3, pady=2)
clear_btn.config(command=clear_entries)
# ===============#

# ====SEARCHING====#

search_frame = tk.Frame(data_frame, bg="#455864",bd=5, relief=tk.GROOVE)
search_frame.pack(side=tk.TOP,fill=tk.X)

search_lbl = tk.Label(search_frame, text="Search", bg="#455864", font=("Arial", 9, "bold"))
search_lbl.grid(row=0, column=0, padx=2, pady=2)

search_in = tk.Label(search_frame, font=("Arial", 9, "bold"),width=38)
search_in.grid(row=0, column=1, padx=3, pady=2)

search_ent = tk.Entry(search_frame, font=("Arial", 9),width=38)
search_ent.insert(0, "Enter ID Number")
search_ent.grid(row=0, column=1, padx=3, pady=2)

def on_search_focus_in(event):
    if search_ent.get() == "Enter ID Number":
        search_ent.delete(0, tk.END)

search_ent.bind("<FocusIn>", on_search_focus_in)


search_btn = tk.Button(search_frame, text="Search", font=("Arial", 8, "bold"), bd=5, width=6, bg="#455864")
search_btn.grid(row=0, column=2, padx=3, pady=2)
search_btn.config(command=search_student)


refresh_btn = tk.Button(search_frame, text="Refresh", font=("Arial", 8, "bold"), bd=5, width=6, bg="#455864", command=refresh_table)
refresh_btn.grid(row=0, column=4, padx=3, pady=2)
refresh_btn.config(command=refresh_table)


# ===================#

main_frame = tk.Frame(data_frame, bg="#455864", bd=5, relief=tk.GROOVE)
main_frame.pack(fill=tk.BOTH, expand=True)

y_scroll = tk.Scrollbar(data_frame, orient=tk.VERTICAL)
x_scroll = tk.Scrollbar(data_frame, orient=tk.HORIZONTAL)

student_table = ttk.Treeview(data_frame, columns=("ID Number","Last Name", "First Name", "Middle Name", "Year Level", "Gender", "Course"),yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

y_scroll.config(command=student_table.yview)
x_scroll.config(command=student_table.xview)

y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

student_table.heading("ID Number", text="ID Number")
student_table.heading("Last Name", text="Last Name")
student_table.heading("First Name", text="First Name")
student_table.heading("Middle Name", text="Middle Name")
student_table.heading("Year Level", text="Year Level")
student_table.heading("Gender", text="Gender")
student_table.heading("Course", text="Course")

student_table['show'] = 'headings'

student_table.column("ID Number", width=100)
student_table.column("Last Name", width=100)
student_table.column("First Name", width=100)
student_table.column("Middle Name", width=100)
student_table.column("Year Level", width=100)
student_table.column("Gender", width=100)
student_table.column("Course", width=100)

student_table.pack(fill=tk.BOTH, expand=True)

student_table.bind("<ButtonRelease-1>", on_student_select)
update_student_table()

def open_view_courses_dialog():
    dialog_window = tk.Toplevel(win)
    dialog_window.title("Available Courses")

    try:
        with open('courses.csv', 'r') as file:
            reader = csv.reader(file)
            courses = [row[0] for row in reader]  
    except FileNotFoundError:
        courses = []

    #display the courses
    listbox = tk.Listbox(dialog_window, font=("Arial", 12), selectmode=tk.SINGLE)
    listbox.pack(padx=20, pady=10)

    for course in courses:
        listbox.insert(tk.END, course)

    def edit_course():
        selected_index = listbox.curselection()
        if selected_index:
            selected_course = listbox.get(selected_index)
            new_course_code = simpledialog.askstring("Edit Course", "Enter new course code:", parent=dialog_window)
            if new_course_code:
                listbox.delete(selected_index)
                listbox.insert(selected_index, new_course_code)
                update_course_in_csv(selected_course, new_course_code)
                update_student_courses(selected_course, new_course_code)
                messagebox.showinfo("Success", "Course updated successfully!")

    edit_button = tk.Button(dialog_window, text="Edit", command=edit_course)
    edit_button.pack(pady=10)

# ===================#

win.mainloop()