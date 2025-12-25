from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class Position(str, Enum):
    PROFESSOR = "Professor"
    ASSOCIATE_PROFESSOR = "Associate Professor"
    ASSISTANT_PROFESSOR = "Assistant Professor"
    LECTURER = "Lecturer"
    HEAD_OF_DEPARTMENT = "Head of Department (HOD)"
    PRINCIPAL = "Principal"
    ACCOUNTANT = "Accountant"
    LIBRARIAN = "Librarian"

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

class Department(str, Enum):
    COMPUTER_SCIENCE = "Computer Science"
    INFORMATION_TECHNOLOGY = "Information Technology"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    CIVIL_ENGINEERING = "Civil Engineering"
    ELECTRONICS_ENGINEERING = "Electronics Engineering"
    MATHEMATICS = "Mathematics"
    PHYSICS = "Physics"
    CHEMISTRY = "Chemistry"
    MANAGEMENT_STUDIES = "Management Studies"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    DATA_SCIENCE = "Data Science"

class Qualification(BaseModel):
    degree: str
    institution: str
    year: int
    specialization: Optional[str] = None
    percentage: Optional[float] = None

class FacultyBase(BaseModel):
    name: str
    email: EmailStr
    position: Position
    stream: Stream
    department: Department
    college_name: str
    photo_url: Optional[str] = None
    mobile_no: str
    employee_id: Optional[str] = None
    qualifications: List[Qualification] = []
    joining_date: Optional[date] = None
    experience_years: Optional[int] = None
    subjects_taught: List[str] = []
    office_hours: Optional[str] = None
    cabin_number: Optional[str] = None
    research_interests: Optional[List[str]] = []

class FacultyCreate(FacultyBase):
    password: str

class FacultyUpdate(BaseModel):
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    position: Optional[Position] = None
    stream: Optional[Stream] = None
    college_name: Optional[str] = None
    photo_url: Optional[str] = None
    employee_id: Optional[str] = None
    qualifications: Optional[List[Qualification]] = None
    experience_years: Optional[int] = None
    subjects_taught: Optional[List[str]] = None
    office_hours: Optional[str] = None
    cabin_number: Optional[str] = None
    research_interests: Optional[List[str]] = None

class FacultyInDB(FacultyBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class FacultyResponse(FacultyBase):
    id: str
    created_at: datetime
    updated_at: datetime