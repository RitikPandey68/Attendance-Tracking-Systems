from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LEAVE = "leave"
    HOLIDAY = "holiday"

class AttendanceCreate(BaseModel):
    student_id: str
    date: date
    period: int
    subject: str
    status: AttendanceStatus

class AttendanceUpdate(BaseModel):
    status: Optional[AttendanceStatus] = None

class AttendanceResponse(BaseModel):
    id: str
    student_id: str
    faculty_id: str
    date: str
    period: int
    subject: str
    status: str
    created_at: datetime
    updated_at: datetime

class AttendanceSummary(BaseModel):
    total_classes: int
    present_count: int
    absent_count: int
    leave_count: int
    holiday_count: int
    attendance_percentage: float

class DailyAttendance(BaseModel):
    date: str
    subject: str
    period: int
    status: str

class WeeklyAttendance(BaseModel):
    week_start: str
    week_end: str
    summary: AttendanceSummary
    daily_attendance: List[DailyAttendance]

class MonthlyAttendance(BaseModel):
    month: str
    year: int
    summary: AttendanceSummary
    daily_attendance: List[AttendanceResponse]

class SubjectAttendanceStats(BaseModel):
    subject: str
    daily_count: int
    weekly_count: int
    monthly_count: int
    total_classes: int
    attended_classes: int
    percentage: float

class OverallAttendanceStats(BaseModel):
    daily_count: int
    weekly_count: int
    monthly_count: int
    total_classes: int
    attended_classes: int
    average_percentage: float