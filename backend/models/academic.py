from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class NoteType(str, Enum):
    LECTURE = "Lecture Notes"
    ASSIGNMENT = "Assignment"
    REFERENCE = "Reference Material"
    SYLLABUS = "Syllabus"
    PRACTICAL = "Practical Notes"

class Note(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    subject: str
    note_type: NoteType
    faculty_id: str
    file_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class NoteCreate(BaseModel):
    title: str
    content: str
    subject: str
    note_type: NoteType
    file_url: Optional[str] = None

class AnnouncementType(str, Enum):
    GENERAL = "General"
    EXAM = "Exam"
    ASSIGNMENT = "Assignment"
    EVENT = "Event"
    HOLIDAY = "Holiday"
    URGENT = "Urgent"

class Announcement(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    announcement_type: AnnouncementType
    faculty_id: str
    target_year: Optional[int] = None
    target_department: Optional[str] = None
    is_urgent: bool = False
    valid_until: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    announcement_type: AnnouncementType
    target_year: Optional[int] = None
    target_department: Optional[str] = None
    is_urgent: bool = False
    valid_until: Optional[date] = None

class ExamType(str, Enum):
    INTERNAL = "Internal"
    LAB = "Lab"
    SEMESTER = "Semester"
    ASSIGNMENT = "Assignment"
    QUIZ = "Quiz"

class ExamSchedule(BaseModel):
    id: Optional[str] = None
    subject: str
    exam_type: ExamType
    exam_date: date
    start_time: str
    end_time: str
    venue: str
    faculty_id: str
    year: int
    department: str
    syllabus: Optional[str] = None
    instructions: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ExamScheduleCreate(BaseModel):
    subject: str
    exam_type: ExamType
    exam_date: date
    start_time: str
    end_time: str
    venue: str
    year: int
    department: str
    syllabus: Optional[str] = None
    instructions: Optional[str] = None

class AssignmentStatus(str, Enum):
    ASSIGNED = "Assigned"
    SUBMITTED = "Submitted"
    GRADED = "Graded"
    LATE = "Late"

class Assignment(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    subject: str
    faculty_id: str
    assigned_date: date
    due_date: date
    max_marks: int
    file_url: Optional[str] = None
    year: int
    department: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AssignmentCreate(BaseModel):
    title: str
    description: str
    subject: str
    assigned_date: date
    due_date: date
    max_marks: int
    file_url: Optional[str] = None
    year: int
    department: str

class AssignmentSubmission(BaseModel):
    id: Optional[str] = None
    assignment_id: str
    student_id: str
    submission_date: datetime
    file_url: Optional[str] = None
    comments: Optional[str] = None
    status: AssignmentStatus
    marks_obtained: Optional[int] = None
    feedback: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AssignmentSubmissionCreate(BaseModel):
    assignment_id: str
    file_url: Optional[str] = None
    comments: Optional[str] = None

class FeeType(str, Enum):
    TUITION = "Tuition Fee"
    EXAM = "Exam Fee"
    LIBRARY = "Library Fee"
    LAB = "Lab Fee"
    HOSTEL = "Hostel Fee"
    TRANSPORT = "Transport Fee"
    MISCELLANEOUS = "Miscellaneous"

class FeeDetail(BaseModel):
    id: Optional[str] = None
    student_id: str
    fee_type: FeeType
    amount: float
    due_date: date
    paid_date: Optional[date] = None
    is_paid: bool = False
    semester: int
    academic_year: str
    late_fee: float = 0.0
    discount: float = 0.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class FeeDetailCreate(BaseModel):
    student_id: str
    fee_type: FeeType
    amount: float
    due_date: date
    semester: int
    academic_year: str
    late_fee: float = 0.0
    discount: float = 0.0

class FeePayment(BaseModel):
    id: Optional[str] = None
    fee_detail_id: str
    amount_paid: float
    payment_date: datetime
    payment_method: str
    transaction_id: Optional[str] = None
    receipt_url: Optional[str] = None
    created_at: Optional[datetime] = None

class FeePaymentCreate(BaseModel):
    fee_detail_id: str
    amount_paid: float
    payment_method: str
    transaction_id: Optional[str] = None
    receipt_url: Optional[str] = None