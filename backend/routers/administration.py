from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date, timedelta
import uuid
from models.administration import *
from core.database import get_database
from routers.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["administration"])

@router.get("/dashboard", response_model=DashboardData)
async def get_dashboard_data(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Only admin can access dashboard")
    
    # Get system statistics
    total_students = db.students.count_documents({})
    total_faculty = db.faculty.count_documents({})
    
    system_stats = SystemStats(
        total_students=total_students,
        total_faculty=total_faculty,
        total_courses=0,
        total_departments=0,
        active_sessions=0,
        pending_fees=0,
        recent_registrations=0
    )
    
    return DashboardData(
        system_stats=system_stats,
        recent_activities=[],
        pending_approvals=[],
        fee_collections={},
        attendance_overview={}
    )