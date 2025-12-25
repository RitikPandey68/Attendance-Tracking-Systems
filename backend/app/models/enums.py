from enum import Enum

class CourseType(str, Enum):
    B_TECH = "B.Tech"
    M_TECH = "M.Tech"
    BBA = "BBA"
    MBA = "MBA"
    BCA = "BCA"
    MCA = "MCA"

class Specialization(str, Enum):
    COMPUTER_SCIENCE = "Computer Science"
    ELECTRICAL = "Electrical Engineering"
    MECHANICAL = "Mechanical Engineering"
    CIVIL = "Civil Engineering"
    ELECTRONICS = "Electronics Engineering"
    BUSINESS = "Business Administration"
    FINANCE = "Finance"
    MARKETING = "Marketing"

class LeaveType(str, Enum):
    SICK_LEAVE = "Sick Leave"
    CASUAL_LEAVE = "Casual Leave"
    MATERNITY_LEAVE = "Maternity Leave"
    EMERGENCY_LEAVE = "Emergency Leave"
    VACATION_LEAVE = "Vacation Leave"
