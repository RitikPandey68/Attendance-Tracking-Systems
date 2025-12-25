from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.database import get_database

app = FastAPI(
    title="AI Powered Attendance Tracking System",
    description="Comprehensive attendance and academic management system",
    version="2.0.0"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection
try:
    get_database()
    print("Database connection successful")
except Exception as e:
    print(f"Database connection error: {e}")
    raise

# Import and include routers
from routers import (
    auth, attendance, results,
    student, faculty
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(attendance.router, tags=["attendance"])
app.include_router(results.router, prefix="/results", tags=["results"])
app.include_router(student.router, tags=["students"])
app.include_router(faculty.router, tags=["faculty"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the AI Powered Attendance Tracking System!",
        "version": "2.0.0",
        "features": [
            "Student Management with complete profile (Name, DOB, USN, Degree, College, Stream, Email-ID, Mobile)",
            "Faculty Management with qualifications (Name, Email-ID, Position, Stream, Department, College, Photo, Mobile, Qualifications)",
            "Daily/Weekly/Monthly Attendance tracking per subject + overall statistics",
            "Notes provision section-wise by faculty",
            "Announcements and notice board",
            "Exam scheduling (Internal & Lab)",
            "Results management (Internal & Lab)",
            "Assignment submissions",
            "Fee management connected to Administration",
            "Complete dashboards for Students, Faculty, and Administration"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
