from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class TestType(str, Enum):
    CLASS_TEST = "class_test"
    PREPARATORY_TEST = "preparatory_test"
    SEMESTER_EXAM = "semester_exam"

class ResultBase(BaseModel):
    student_id: str
    test_type: TestType
    subject: str
    marks_obtained: float
    total_marks: float
    test_date: datetime
    semester: int

class ResultCreate(ResultBase):
    faculty_id: Optional[str] = None

class ResultUpdate(BaseModel):
    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = None
    test_date: Optional[datetime] = None

class ResultInDB(ResultBase):
    id: str
    faculty_id: str
    created_at: datetime
    updated_at: datetime

class ResultResponse(ResultBase):
    id: str
    faculty_id: str
    percentage: float
    grade: str
    created_at: datetime
    updated_at: datetime

class SubjectResult(BaseModel):
    subject: str
    results: List[ResultResponse]
    average_percentage: float

class SemesterResultSummary(BaseModel):
    semester: int
    subjects: List[SubjectResult]
    overall_percentage: float
    cgpa: float

class TestResultSummary(BaseModel):
    test_type: TestType
    results: List[ResultResponse]
    average_percentage: float
