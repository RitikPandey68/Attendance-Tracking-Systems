from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime, date
from enum import Enum

class AdminRole(str, Enum):
    SUPER_ADMIN = "Super Admin"
    ACADEMIC_ADMIN = "Academic Admin"
    FINANCE_ADMIN = "Finance Admin"
    STUDENT_ADMIN = "Student Admin"
    FACULTY_ADMIN = "Faculty Admin"

class AdminBase(BaseModel):
    name: str
    email: EmailStr
    mobile_no: str
    role: AdminRole
    department: Optional[str] = None
    employee_id: Optional[str] = None
    photo_url: Optional[str] = None

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    role: Optional[AdminRole] = None
    department: Optional[str] = None
    employee_id: Optional[str] = None
    photo_url: Optional[str] = None

class AdminInDB(AdminBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class AdminResponse(AdminBase):
    id: str
    created_at: datetime
    updated_at: datetime

class SystemStats(BaseModel):
    total_students: int
    total_faculty: int
    total_courses: int
    total_departments: int
    active_sessions: int
    pending_fees: float
    recent_registrations: int

class DashboardData(BaseModel):
    system_stats: SystemStats
    recent_activities: List[Dict]
    pending_approvals: List[Dict]
    fee_collections: Dict[str, float]
    attendance_overview: Dict[str, float]

class CollegeInfo(BaseModel):
    id: Optional[str] = None
    name: str
    address: str
    phone: str
    email: EmailStr
    website: Optional[str] = None
    established_year: Optional[int] = None
    affiliation: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CollegeInfoCreate(BaseModel):
    name: str
    address: str
    phone: str
    email: EmailStr
    website: Optional[str] = None
    established_year: Optional[int] = None
    affiliation: Optional[str] = None
    logo_url: Optional[str] = None

class AcademicYear(BaseModel):
    id: Optional[str] = None
    year: str  # e.g., "2024-25"
    start_date: date
    end_date: date
    is_current: bool = False
    created_at: Optional[datetime] = None

class AcademicYearCreate(BaseModel):
    year: str
    start_date: date
    end_date: date
    is_current: bool = False

class Semester(BaseModel):
    id: Optional[str] = None
    name: str  # e.g., "Semester 1", "Semester 2"
    academic_year_id: str
    start_date: date
    end_date: date
    is_current: bool = False
    created_at: Optional[datetime] = None

class SemesterCreate(BaseModel):
    name: str
    academic_year_id: str
    start_date: date
    end_date: date
    is_current: bool = False