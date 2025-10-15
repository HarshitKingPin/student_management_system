import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'student_management'
        self.user = 'root'  # Change this to your MySQL username
        self.password = 'Harshit@1221'   # Change this to your MySQL password
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Create database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("✅ Successfully connected to database")
        except Error as e:
            print(f"❌ Error: {e}")
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("🔒 Database connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a query that modifies data"""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"❌ Error executing query: {e}")
            self.connection.rollback()
            return False
    
    def fetch_query(self, query, params=None):
        """Execute a query that fetches data"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"❌ Error fetching data: {e}")
            return None