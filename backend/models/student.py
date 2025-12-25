from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import date, datetime
from enum import Enum

class CourseType(str, Enum):
    B_TECH = "B.Tech"
    M_TECH = "M.Tech"
    BBA = "BBA"
    MBA = "MBA"
    B_E = "B.E"
    BCA = "BCA"
    MCA = "MCA"
    B_SC = "B.Sc"
    M_SC = "M.Sc"
    DIPLOMA = "Diploma"

class Stream(str, Enum):
    COMPUTER_SCIENCE = "Computer Science"
    INFORMATION_TECHNOLOGY = "Information Technology"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    CIVIL_ENGINEERING = "Civil Engineering"
    ELECTRONICS_ENGINEERING = "Electronics Engineering"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    DATA_SCIENCE = "Data Science"
    CYBERSECURITY = "Cybersecurity"
    BUSINESS_ADMINISTRATION = "Business Administration"
    FINANCE = "Finance"
    MARKETING = "Marketing"

class StudentBase(BaseModel):
    name: str
    dob: date
    usn: str
    degree: CourseType
    college: str
    stream: Stream
    email: EmailStr
    mobile_no: str
    father_name: str
    mother_name: str
    address: str
    year: int
    photo_url: Optional[str] = None
    emergency_contact: Optional[str] = None
    blood_group: Optional[str] = None
    admission_date: Optional[date] = None
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None

class StudentCreate(BaseModel):
    name: str
    dob: date
    usn: str
    degree: str  # Changed from CourseType to str for flexibility
    college: str
    stream: str  # Changed from Stream to str for flexibility
    email: EmailStr
    mobile_no: str
    father_name: str
    mother_name: str
    address: str
    year: int
    password: str
    course: Optional[str] = None  # For compatibility
    specialization: Optional[str] = None  # For compatibility
    photo_url: Optional[str] = None
    emergency_contact: Optional[str] = None
    blood_group: Optional[str] = None
    admission_date: Optional[date] = None
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    address: Optional[str] = None
    photo_url: Optional[str] = None
    emergency_contact: Optional[str] = None
    blood_group: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None

class SubjectAttendance(BaseModel):
    subject: str
    daily_count: int = 0
    weekly_count: int = 0
    monthly_count: int = 0
    total_classes: int = 0
    attended_classes: int = 0
    percentage: float = 0.0

class OverallAttendance(BaseModel):
    daily_count: int = 0
    weekly_count: int = 0
    monthly_count: int = 0
    total_classes: int = 0
    attended_classes: int = 0
    average_percentage: float = 0.0

class ExamResult(BaseModel):
    subject: str
    exam_type: str  # "internal" or "lab"
    marks_obtained: int
    total_marks: int
    percentage: float
    grade: str
    exam_date: date

class SemesterResult(BaseModel):
    semester: int
    cgpa: float
    subjects: List[ExamResult] = []
    internal_results: List[ExamResult] = []
    lab_results: List[ExamResult] = []

class StudentInDB(StudentBase):
    id: str
    user_id: str
    semester_results: List[SemesterResult] = []
    total_cgpa: float = 0.0
    subject_attendance: List[SubjectAttendance] = []
    overall_attendance: OverallAttendance = OverallAttendance()
    created_at: datetime
    updated_at: datetime

class StudentResponse(StudentBase):
    id: str
    total_cgpa: float
    semester_results: List[SemesterResult]
    subject_attendance: List[SubjectAttendance]
    overall_attendance: OverallAttendance
    created_at: datetime
    updated_at: datetime
