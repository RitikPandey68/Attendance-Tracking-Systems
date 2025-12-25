from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
import uuid
from pydantic import BaseModel
from core.database import get_database
from routers.auth import get_current_user

router = APIRouter()

class ResultCreate(BaseModel):
    student_id: str
    subject: str
    test_type: str  # "internal" or "lab"
    test_date: date
    marks_obtained: int
    total_marks: int
    semester: int
    grade: Optional[str] = None

class ResultResponse(BaseModel):
    id: str
    student_id: str
    subject: str
    test_type: str
    test_date: date
    marks_obtained: int
    total_marks: int
    percentage: float
    grade: str
    semester: int
    created_at: datetime

@router.post("/create", response_model=ResultResponse)
async def create_result(
    result: ResultCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Only faculty and admin can create results")
    
    # Calculate percentage and grade
    percentage = (result.marks_obtained / result.total_marks) * 100
    
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B+"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"
    
    result_data = result.dict()
    result_data.update({
        "id": str(uuid.uuid4()),
        "percentage": percentage,
        "grade": grade,
        "test_date": str(result.test_date),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    })
    
    db.results.insert_one(result_data)
    return ResultResponse(**result_data)

@router.get("/student/{student_id}")
async def get_student_results(
    student_id: str,
    test_type: Optional[str] = None,
    semester: Optional[int] = None,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    # Students can only view their own results
    if current_user["role"] == "student":
        student = db.students.find_one({"user_id": current_user["id"]})
        if not student or student["id"] != student_id:
            raise HTTPException(status_code=403, detail="Can only view your own results")
    
    query = {"student_id": student_id}
    if test_type:
        query["test_type"] = test_type
    if semester:
        query["semester"] = semester
    
    results = list(db.results.find(query).sort("test_date", -1))
    return [ResultResponse(**result) for result in results]

@router.get("/internal/{student_id}")
async def get_internal_results(
    student_id: str,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    return await get_student_results(student_id, "internal", None, current_user, db)

@router.get("/lab/{student_id}")
async def get_lab_results(
    student_id: str,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    return await get_student_results(student_id, "lab", None, current_user, db)

@router.get("/semester/{student_id}/{semester}")
async def get_semester_results(
    student_id: str,
    semester: int,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    return await get_student_results(student_id, None, semester, current_user, db)

@router.put("/{result_id}")
async def update_result(
    result_id: str,
    result_update: ResultCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Only faculty and admin can update results")
    
    existing_result = db.results.find_one({"id": result_id})
    if not existing_result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Calculate new percentage and grade
    percentage = (result_update.marks_obtained / result_update.total_marks) * 100
    
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B+"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 50:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"
    
    update_data = result_update.dict()
    update_data.update({
        "percentage": percentage,
        "grade": grade,
        "test_date": str(result_update.test_date),
        "updated_at": datetime.now()
    })
    
    db.results.update_one({"id": result_id}, {"$set": update_data})
    updated_result = db.results.find_one({"id": result_id})
    
    return ResultResponse(**updated_result)

@router.delete("/{result_id}")
async def delete_result(
    result_id: str,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Only faculty and admin can delete results")
    
    result = db.results.find_one({"id": result_id})
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    db.results.delete_one({"id": result_id})
    return {"message": "Result deleted successfully"}