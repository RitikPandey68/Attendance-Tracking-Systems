from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict
from bson import ObjectId
import uuid

from core.database import get_database
from models.attendance import (
    AttendanceCreate, AttendanceResponse, AttendanceUpdate,
    AttendanceSummary, MonthlyAttendance, WeeklyAttendance
)
from routers.auth import get_current_user

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/enroll", response_model=AttendanceResponse)
async def enroll_attendance(
    attendance_data: AttendanceCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] != "faculty":
        raise HTTPException(status_code=403, detail="Only faculty can enroll attendance")
    
    attendance_dict = attendance_data.dict()
    attendance_dict["id"] = str(uuid.uuid4())
    attendance_dict["faculty_id"] = current_user["id"]
    attendance_dict["date"] = str(attendance_data.date)
    attendance_dict["created_at"] = datetime.now()
    attendance_dict["updated_at"] = datetime.now()
    
    db.attendance.insert_one(attendance_dict)
    return AttendanceResponse(**attendance_dict)