from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import uuid
import hashlib
from models.student import StudentCreate, StudentInDB
from models.faculty import FacultyCreate, FacultyInDB
from core.database import get_database
from core.config import settings
from app.services.emailer import send_verification_email

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "your-secret-key-here-for-jwt-tokens"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})
    # Simple token creation without JWT library
    import json
    import base64
    token_data = json.dumps(to_encode)
    encoded_token = base64.b64encode(token_data.encode()).decode()
    return encoded_token

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        import json
        import base64
        token_data = json.loads(base64.b64decode(token.encode()).decode())
        user_id: str = token_data.get("sub")
        if user_id is None:
            raise credentials_exception
        # Check token expiry
        exp = token_data.get("exp")
        if exp and datetime.utcnow().timestamp() > exp:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    # Check in users collection
    user = db.users.find_one({"id": user_id})
    if user is None:
        raise credentials_exception
    return user

@router.post("/register/student")
async def register_student(student: StudentCreate, db = Depends(get_database)):
    # Check if user already exists
    if db.users.find_one({"email": student.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if db.students.find_one({"usn": student.usn}):
        raise HTTPException(status_code=400, detail="USN already registered")
    
    # Create user account
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(student.password)
    
    user_data = {
        "id": user_id,
        "email": student.email,
        "hashed_password": hashed_password,
        "role": "student",
        "is_active": True,
        "created_at": datetime.now()
    }
    
    # Create student profile
    student_dict = student.dict()
    del student_dict["password"]
    student_dict.update({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "subject_attendance": [],
        "overall_attendance": {
            "daily_count": 0,
            "weekly_count": 0,
            "monthly_count": 0,
            "total_classes": 0,
            "attended_classes": 0,
            "average_percentage": 0.0
        },
        "semester_results": [],
        "total_cgpa": 0.0,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    
    db.users.insert_one(user_data)
    db.students.insert_one(student_dict)
    
    return {"message": "Student registered successfully", "user_id": user_id}

@router.post("/register/faculty")
async def register_faculty(faculty: FacultyCreate, db = Depends(get_database)):
    # Check if user already exists
    if db.users.find_one({"email": faculty.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user account
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(faculty.password)
    
    user_data = {
        "id": user_id,
        "email": faculty.email,
        "hashed_password": hashed_password,
        "role": "faculty",
        "is_active": True,
        "created_at": datetime.now()
    }
    
    # Create faculty profile
    faculty_dict = faculty.dict()
    del faculty_dict["password"]
    faculty_dict.update({
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    
    db.users.insert_one(user_data)
    db.faculty.insert_one(faculty_dict)

    # Send verification email
    verification_link = f"http://localhost:8501/verify-email?token={user_id}&role=faculty"
    try:
        await send_verification_email(faculty.email, verification_link)
        return {"message": "Faculty registered successfully. Please check your email for verification.", "user_id": user_id}
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        return {"message": "Faculty registered successfully, but email verification failed. Please contact support.", "user_id": user_id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_database)):
    user = db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile")
async def get_profile(current_user = Depends(get_current_user), db = Depends(get_database)):
    if current_user["role"] == "student":
        student = db.students.find_one({"user_id": current_user["id"]})
        if student:
            student["role"] = "student"
            return student
    elif current_user["role"] == "faculty":
        faculty = db.faculty.find_one({"user_id": current_user["id"]})
        if faculty:
            faculty["role"] = "faculty"
            return faculty
    
    raise HTTPException(status_code=404, detail="Profile not found")