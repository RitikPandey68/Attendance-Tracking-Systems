from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date, timedelta
import uuid
from models.student import *
from models.academic import *
from core.database import get_database
from routers.auth import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=List[StudentResponse])
async def get_all_students(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Only faculty and admin can view all students")
    
    students = list(db.students.find({}))
    return [StudentResponse(**student) for student in students]

@router.get("/me", response_model=StudentResponse)
async def get_my_profile(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] != "student":
        raise HTTPException(status_code=403, detail="Only students can access this endpoint")
    
    student = db.students.find_one({"user_id": current_user["id"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    
    return StudentResponse(**student)