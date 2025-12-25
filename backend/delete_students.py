from core.database import get_database
from models.student import Student

def delete_all_students():
    db = get_database()
    result = db.students.delete_many({})
    print(f"Deleted {result.deleted_count} students")

if __name__ == "__main__":
    delete_all_students()
