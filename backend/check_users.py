from core.database import get_db
from bson import ObjectId

def check_users():
    db = get_db()
    users_collection = db.get_collection("users")
    
    # Check all users
    users = list(users_collection.find())
    print(f"Total users in database: {len(users)}")
    
    for user in users:
        print(f"User ID: {user['_id']}")
        print(f"Email: {user.get('email', 'N/A')}")
        print(f"Role: {user.get('role', 'N/A')}")
        print(f"Student ID: {user.get('student_id', 'N/A')}")
        print("---")
    
    # Check the specific student user
    student_email = "john.doe9816@example.com"
    student_user = users_collection.find_one({"email": student_email})
    if student_user:
        print(f"Student user {student_email} exists!")
        print(f"Student user details: {student_user}")
        
        # Check if there's a student record linked to this user
        students_collection = db.get_collection("students")
        student_record = students_collection.find_one({"_id": ObjectId(student_user["_id"])})
        if student_record:
            print(f"Student record found for user: {student_record}")
        else:
            print(f"No student record found for user ID: {student_user['_id']}")
    else:
        print(f"Student user {student_email} does NOT exist!")

if __name__ == "__main__":
    check_users()
