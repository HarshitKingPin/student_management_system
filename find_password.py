import mysql.connector
from mysql.connector import Error
import getpass

def find_mysql_password():
    """Try to find working MySQL credentials"""
    
    print("=" * 60)
    print("🔍 MySQL PASSWORD FINDER")
    print("=" * 60)
    
    # Common default passwords to try
    common_passwords = [
        '',           # Empty (XAMPP default)
        'root',       # Common default
        'password',   # Common default
        'admin',      # Common default
        'mysql',      # Common default
        '123456',     # Common weak password
        'Password123', # Common default
    ]
    
    print("\n📝 Trying common passwords...\n")
    
    # Try each password
    for pwd in common_passwords:
        display_pwd = '(empty)' if pwd == '' else pwd
        print(f"Testing password: {display_pwd}... ", end='')
        
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password=pwd
            )
            
            if connection.is_connected():
                print("✅ SUCCESS!")
                print("\n" + "=" * 60)
                print("🎉 FOUND WORKING PASSWORD!")
                print("=" * 60)
                print(f"\n📋 Your MySQL credentials:")
                print(f"   Username: root")
                print(f"   Password: {display_pwd}")
                
                print(f"\n📝 Update your database.py file:")
                print(f"   Line 9: self.password = '{pwd}'")
                
                # Test database creation
                cursor = connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS student_management")
                cursor.execute("USE student_management")
                print(f"\n✅ Database 'student_management' is ready!")
                
                cursor.close()
                connection.close()
                return pwd
                
        except Error:
            print("❌ Failed")
            continue
    
    print("\n" + "=" * 60)
    print("❌ No common passwords worked")
    print("=" * 60)
    
    # Ask user to input password
    print("\n🔑 Let's try your password manually...")
    print("   (If you don't remember, we'll help you reset it)\n")
    
    for attempt in range(3):
        user_pwd = input(getpass.getpass("Enter your MySQL password (or press Enter for empty): "))
        
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password=user_pwd
            )
            
            if connection.is_connected():
                print("\n✅ SUCCESS! That password works!")
                print(f"\n📝 Update your database.py file:")
                print(f"   Line 9: self.password = '{user_pwd}'")
                connection.close()
                return user_pwd
                
        except Error as e:
            print(f"❌ Failed: {e}")
            if attempt < 2:
                print("Try again...\n")
    
    print("\n🔧 Password not found. Let's reset it...")
    return None

def show_reset_instructions():
    """Show how to reset MySQL password"""
    print("\n" + "=" * 60)
    print("📚 HOW TO RESET YOUR MySQL PASSWORD")
    print("=" * 60)
    
    print("""
Option 1: REINSTALL WITH XAMPP (Easiest)
=========================================
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Use XAMPP MySQL (no password by default)
4. Update database.py: self.password = ''

Option 2: RESET MySQL PASSWORD (Windows)
========================================
1. Open Command Prompt as Administrator
2. Stop MySQL service:
   net stop MySQL80
   
3. Create reset file C:\\mysql-reset.txt with:
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword123';
   
4. Run MySQL with reset file:
   cd "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin"
   mysqld --init-file=C:\\mysql-reset.txt
   
5. Restart MySQL service:
   net start MySQL80
   
6. Update database.py: self.password = 'newpassword123'

Option 3: USE MySQL WORKBENCH
==============================
1. Open MySQL Workbench
2. If it connects, it saved your password
3. Click: Server → Users and Privileges
4. Reset root password there
""")

if __name__ == "__main__":
    password = find_mysql_password()
    
    if password is None:
        show_reset_instructions()
    else:
        print("\n✅ You can now run: python main.py")