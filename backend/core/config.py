import os

class Settings:
    MONGODB_URL: str = "mongodb://localhost:27017"
    SECRET_KEY: str = "your-secret-key-here-for-jwt-tokens"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    
    # Frontend URL for email verification
    FRONTEND_URL: str = "http://localhost:8501"

settings = Settings()

# Database names
ATTENDANCE_DB = "attendance_db"
USERS_COLLECTION = "users"
STUDENTS_COLLECTION = "students"
FACULTY_COLLECTION = "faculty"
ATTENDANCE_COLLECTION = "attendance"
RESULTS_COLLECTION = "results"
