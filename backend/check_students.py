from core.database import get_db
from bson import ObjectId

def check_students():
    db = get_db()
    students_collection = db.get_collection("students")
    
    # Check if any students exist
    students = list(students_collection.find())
    print(f"Total students in database: {len(students)}")
    
    for student in students:
        print(f"Student ID: {student['_id']}")
        print(f"Name: {student.get('name', 'N/A')}")
        print(f"Email: {student.get('email', 'N/A')}")
        print(f"User ID: {student.get('user_id', 'N/A')}")
        print("---")
    
    # Check if the specific student ID exists
    test_student_id = "68ac9c320a1edb72993d3627"
    student = students_collection.find_one({"_id": ObjectId(test_student_id)})
    if student:
        print(f"Test student ID {test_student_id} exists!")
        print(f"Student details: {student}")
    else:
        print(f"Test student ID {test_student_id} does NOT exist!")

if __name__ == "__main__":
    check_students()
