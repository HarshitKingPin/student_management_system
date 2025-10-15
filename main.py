import tkinter as tk
from tkinter import ttk, messagebox
from student_model import StudentModel

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize model
        self.model = StudentModel()
        
        # Variables
        self.selected_student_id = None
        self.setup_variables()
        
        # Create GUI
        self.create_widgets()
        
        # Load initial data
        self.load_students()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_variables(self):
        """Setup StringVar variables for form fields"""
        self.var_roll = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_age = tk.StringVar()
        self.var_grade = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_marks = tk.StringVar()
        self.var_search = tk.StringVar()
        self.var_search_by = tk.StringVar(value="Roll Number")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🎓 Student Management System",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Frame - Form
        left_frame = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Form Title
        form_title = tk.Label(
            left_frame,
            text="Student Details",
            font=('Arial', 16, 'bold'),
            bg='white'
        )
        form_title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Form Fields
        fields = [
            ("Roll Number:", self.var_roll),
            ("Name:", self.var_name),
            ("Age:", self.var_age),
            ("Grade:", self.var_grade),
            ("Email:", self.var_email),
            ("Phone:", self.var_phone),
            ("Address:", self.var_address),
            ("Marks:", self.var_marks)
        ]
        
        for i, (label, var) in enumerate(fields, start=1):
            tk.Label(
                left_frame,
                text=label,
                font=('Arial', 10),
                bg='white',
                anchor='w'
            ).grid(row=i, column=0, padx=20, pady=5, sticky='w')
            
            if label == "Address:":
                entry = tk.Text(left_frame, height=3, width=25, font=('Arial', 10))
                entry.grid(row=i, column=1, padx=20, pady=5)
                # Bind text widget to variable
                entry.bind('<KeyRelease>', lambda e: self.var_address.set(
                    entry.get('1.0', 'end-1c')
                ))
                self.address_text = entry
            else:
                entry = tk.Entry(left_frame, textvariable=var, font=('Arial', 10), width=25)
                entry.grid(row=i, column=1, padx=20, pady=5)
        
        # Buttons Frame
        button_frame = tk.Frame(left_frame, bg='white')
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        buttons = [
            ("Add", self.add_student, '#27ae60'),
            ("Update", self.update_student, '#3498db'),
            ("Delete", self.delete_student, '#e74c3c'),
            ("Clear", self.clear_form, '#95a5a6')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('Arial', 10, 'bold'),
                width=10,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Right Frame - Search and Table
        right_frame = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Search Frame
        search_frame = tk.Frame(right_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            search_frame,
            text="Search:",
            font=('Arial', 10),
            bg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.var_search,
            font=('Arial', 10),
            width=20
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_combo = ttk.Combobox(
            search_frame,
            textvariable=self.var_search_by,
            values=["Roll Number", "Name"],
            state='readonly',
            width=12
        )
        search_combo.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.search_student,
            bg='#3498db',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            search_frame,
            text="Refresh",
            command=self.load_students,
            bg='#27ae60',
            fg='white',
            font=('Arial', 10),
            cursor='hand2'
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Table Frame
        table_frame = tk.Frame(right_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Roll', 'Name', 'Age', 'Grade', 'Email', 'Phone', 'Marks'),
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Pack scrollbars
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Define headings
        headings = {
            'ID': (50, 'ID'),
            'Roll': (100, 'Roll Number'),
            'Name': (150, 'Name'),
            'Age': (50, 'Age'),
            'Grade': (80, 'Grade'),
            'Email': (150, 'Email'),
            'Phone': (100, 'Phone'),
            'Marks': (80, 'Marks')
        }
        
        for col, (width, text) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, minwidth=50)
        
        # Bind double click
        self.tree.bind('<Double-Button-1>', self.on_tree_select)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def load_students(self):
        """Load all students into the table"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all students
        students = self.model.get_all_students()
        
        if students:
            for student in students:
                self.tree.insert('', 'end', values=(
                    student['id'],
                    student['roll_number'],
                    student['name'],
                    student['age'],
                    student['grade'],
                    student['email'],
                    student['phone'],
                    student['marks']
                ))
    
    def add_student(self):
        """Add a new student"""
        if not self.validate_form():
            return
        
        try:
            success = self.model.add_student(
                self.var_roll.get(),
                self.var_name.get(),
                int(self.var_age.get()),
                self.var_grade.get(),
                self.var_email.get(),
                self.var_phone.get(),
                self.var_address.get(),
                float(self.var_marks.get())
            )
            
            if success:
                messagebox.showinfo("Success", "Student added successfully!")
                self.clear_form()
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to add student. Roll number might already exist.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_student(self):
        """Update selected student"""
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Please select a student to update")
            return
        
        if not self.validate_form():
            return
        
        try:
            success = self.model.update_student(
                self.selected_student_id,
                self.var_roll.get(),
                self.var_name.get(),
                int(self.var_age.get()),
                self.var_grade.get(),
                self.var_email.get(),
                self.var_phone.get(),
                self.var_address.get(),
                float(self.var_marks.get())
            )
            
            if success:
                messagebox.showinfo("Success", "Student updated successfully!")
                self.clear_form()
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to update student")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def delete_student(self):
        """Delete selected student"""
        if not self.selected_student_id:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            success = self.model.delete_student(self.selected_student_id)
            
            if success:
                messagebox.showinfo("Success", "Student deleted successfully!")
                self.clear_form()
                self.load_students()
            else:
                messagebox.showerror("Error", "Failed to delete student")
    
    def search_student(self):
        """Search for students"""
        search_term = self.var_search.get()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Search based on selected option
        if self.var_search_by.get() == "Roll Number":
            students = self.model.search_by_roll_number(search_term)
        else:
            students = self.model.search_by_name(search_term)
        
        if students:
            for student in students:
                self.tree.insert('', 'end', values=(
                    student['id'],
                    student['roll_number'],
                    student['name'],
                    student['age'],
                    student['grade'],
                    student['email'],
                    student['phone'],
                    student['marks']
                ))
        else:
            messagebox.showinfo("Info", "No students found")
    
    def on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            if values:
                self.selected_student_id = values[0]
                
                # Get full student details
                student = self.model.get_student_by_id(self.selected_student_id)
                
                if student:
                    # Fill form
                    self.var_roll.set(student['roll_number'])
                    self.var_name.set(student['name'])
                    self.var_age.set(student['age'])
                    self.var_grade.set(student['grade'])
                    self.var_email.set(student['email'] or '')
                    self.var_phone.set(student['phone'] or '')
                    self.var_address.set(student['address'] or '')
                    self.var_marks.set(student['marks'])
                    
                    # Update address text widget
                    self.address_text.delete('1.0', tk.END)
                    self.address_text.insert('1.0', student['address'] or '')
    
    def clear_form(self):
        """Clear all form fields"""
        self.var_roll.set('')
        self.var_name.set('')
        self.var_age.set('')
        self.var_grade.set('')
        self.var_email.set('')
        self.var_phone.set('')
        self.var_address.set('')
        self.var_marks.set('')
        self.address_text.delete('1.0', tk.END)
        self.selected_student_id = None
    
    def validate_form(self):
        """Validate form inputs"""
        if not self.var_roll.get():
            messagebox.showwarning("Warning", "Roll number is required")
            return False
        
        if not self.var_name.get():
            messagebox.showwarning("Warning", "Name is required")
            return False
        
        try:
            if self.var_age.get():
                age = int(self.var_age.get())
                if age < 1 or age > 100:
                    messagebox.showwarning("Warning", "Please enter a valid age (1-100)")
                    return False
        except ValueError:
            messagebox.showwarning("Warning", "Age must be a number")
            return False
        
        try:
            if self.var_marks.get():
                marks = float(self.var_marks.get())
                if marks < 0 or marks > 100:
                    messagebox.showwarning("Warning", "Marks should be between 0 and 100")
                    return False
        except ValueError:
            messagebox.showwarning("Warning", "Marks must be a number")
            return False
        
        return True
    
    def on_closing(self):
        """Handle window close event"""
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.model.close_connection()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()