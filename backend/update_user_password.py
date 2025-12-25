from pymongo import MongoClient
from passlib.context import CryptContext
from core.config import settings  # Changed to absolute import

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def update_password(email: str, new_password: str):
    client = MongoClient(settings.MONGODB_URL)
    db = client[settings.ATTENDANCE_DB]
    users_collection = db["users"]

    hashed_password = pwd_context.hash(new_password)
    result = users_collection.update_one(
        {"email": email},
        {"$set": {"hashed_password": hashed_password}}
    )
    
    if result.modified_count > 0:
        print(f"Password updated successfully for {email}.")
    else:
        print(f"No user found with email: {email}.")

if __name__ == "__main__":
    update_password("pandeyritikkumar2001@gmail.com", "Anilkp@111")
