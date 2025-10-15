from database import Database

class StudentModel:
    def __init__(self):
        self.db = Database()
    
    def add_student(self, roll_number, name, age, grade, email, phone, address, marks):
        """Add a new student"""
        query = """
            INSERT INTO students (roll_number, name, age, grade, email, phone, address, marks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (roll_number, name, age, grade, email, phone, address, marks)
        return self.db.execute_query(query, params)
    
    def update_student(self, student_id, roll_number, name, age, grade, email, phone, address, marks):
        """Update student details"""
        query = """
            UPDATE students 
            SET roll_number=%s, name=%s, age=%s, grade=%s, 
                email=%s, phone=%s, address=%s, marks=%s
            WHERE id=%s
        """
        params = (roll_number, name, age, grade, email, phone, address, marks, student_id)
        return self.db.execute_query(query, params)
    
    def delete_student(self, student_id):
        """Delete a student"""
        query = "DELETE FROM students WHERE id=%s"
        return self.db.execute_query(query, (student_id,))
    
    def get_all_students(self):
        """Get all students"""
        query = "SELECT * FROM students ORDER BY roll_number"
        return self.db.fetch_query(query)
    
    def search_by_roll_number(self, roll_number):
        """Search student by roll number"""
        query = "SELECT * FROM students WHERE roll_number LIKE %s"
        return self.db.fetch_query(query, (f"%{roll_number}%",))
    
    def search_by_name(self, name):
        """Search student by name"""
        query = "SELECT * FROM students WHERE name LIKE %s"
        return self.db.fetch_query(query, (f"%{name}%",))
    
    def get_student_by_id(self, student_id):
        """Get student by ID"""
        query = "SELECT * FROM students WHERE id=%s"
        result = self.db.fetch_query(query, (student_id,))
        return result[0] if result else None
    
    def close_connection(self):
        """Close database connection"""
        self.db.disconnect()