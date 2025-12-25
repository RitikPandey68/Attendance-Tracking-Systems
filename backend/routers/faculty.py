from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date, timedelta
import uuid
from models.faculty import *
from models.academic import *
from core.database import get_database
from routers.auth import get_current_user

router = APIRouter(prefix="/faculty", tags=["faculty"])

@router.get("/", response_model=List[FacultyResponse])
async def get_all_faculty(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Only faculty and admin can view all faculty")
    
    faculty = list(db.faculty.find({}))
    return [FacultyResponse(**fac) for fac in faculty]

@router.get("/me", response_model=FacultyResponse)
async def get_my_profile(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] != "faculty":
        raise HTTPException(status_code=403, detail="Only faculty can access this endpoint")
    
    faculty = db.faculty.find_one({"user_id": current_user["id"]})
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    
    return FacultyResponse(**faculty)