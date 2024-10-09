import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Create a table for students if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    course TEXT,
    grade TEXT
)
''')

# Commit the changes
conn.commit()

# Function to add a new student record
def add_student(name, age, course, grade):
    cursor.execute('''
    INSERT INTO students (name, age, course, grade)
    VALUES (?, ?, ?, ?)
    ''', (name, age, course, grade))
    conn.commit()
    print(f"Student {name} added successfully!")

# Function to view all student records
def view_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    if students:
        print("-----------------------------------------------------")
        print("Student Records:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Course: {student[3]}, Grade: {student[4]}")
        print("-----------------------------------------------------")

    else:
        print("No students found!")

# Function to update student details by ID
def update_student(student_id, name=None, age=None, course=None, grade=None):
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()
    if student:
        new_name = name if name else student[1]
        new_age = age if age else student[2]
        new_course = course if course else student[3]
        new_grade = grade if grade else student[4]
        cursor.execute('''
        UPDATE students
        SET name = ?, age = ?, course = ?, grade = ?
        WHERE student_id = ?
        ''', (new_name, new_age, new_course, new_grade, student_id))
        conn.commit()
        print(f"Student ID {student_id} updated successfully!")
    else:
        print(f"Student ID {student_id} not found.")

# Function to delete a student record by ID
def delete_student(student_id):
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()
    if student:
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        conn.commit()
        print(f"Student ID {student_id} deleted successfully!")
    else:
        print(f"Student ID {student_id} not found.")

# Function to search for a student by name
def search_student_by_name(name):
    cursor.execute('SELECT * FROM students WHERE name LIKE ?', ('%' + name + '%',))
    students = cursor.fetchall()
    if students:
        print("--------------------------------------------------------")

        print("Search Results:")
        for student in students:
            print(f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Course: {student[3]}, Grade: {student[4]}")
        print("--------------------------------------------------------")

    else:

        print(f"No students found with name {name}.")

# Main Menu
def main():
    while True:
        print("\nStudent Management System")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search Student by Name")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            name = input("Enter student name: ")
            age = int(input("Enter student age: "))
            course = input("Enter student course: ")
            grade = input("Enter student grade: ")
            add_student(name, age, course, grade)
        
        elif choice == '2':
            view_students()
        
        elif choice == '3':
            student_id = int(input("Enter student ID to update: "))
            name = input("Enter new name (press Enter to skip): ")
            age = input("Enter new age (press Enter to skip): ")
            course = input("Enter new course (press Enter to skip): ")
            grade = input("Enter new grade (press Enter to skip): ")
            update_student(student_id, name=name if name else None, age=int(age) if age else None, course=course if course else None, grade=grade if grade else None)
        
        elif choice == '4':
            student_id = int(input("Enter student ID to delete: "))
            delete_student(student_id)
        
        elif choice == '5':
            name = input("Enter name to search: ")
            search_student_by_name(name)
        
        elif choice == '6':
            print("Exiting Student Management System.")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()

# Close the database connection when done
conn.close()
