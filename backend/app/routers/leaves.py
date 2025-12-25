from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date
from pydantic import BaseModel
from backend.core.database import get_db
from backend.app.models.enums import LeaveType

router = APIRouter()

class LeaveApplication(BaseModel):
    usn: str
    leave_type: LeaveType
    reason: str
    start_date: date
    end_date: date
    status: str = "Pending"

class LeaveResponse(BaseModel):
    id: str
    usn: str
    leave_type: LeaveType
    reason: str
    start_date: date
    end_date: date
    status: str
    applied_date: date

@router.post("/", response_model=LeaveResponse)
async def apply_leave(leave: LeaveApplication):
    db = get_db()
    leave_data = leave.dict()
    leave_data["applied_date"] = date.today()
    
    result = db.get_collection("leaves").insert_one(leave_data)
    leave_data["id"] = str(result.inserted_id)
    
    return leave_data

@router.get("/{usn}", response_model=List[LeaveResponse])
async def get_leaves(usn: str):
    db = get_db()
    leaves = list(db.get_collection("leaves").find({"usn": usn}))
    
    for leave in leaves:
        leave["id"] = str(leave["_id"])
        del leave["_id"]
    
    return leaves

@router.get("/", response_model=List[LeaveResponse])
async def get_all_leaves():
    db = get_db()
    leaves = list(db.get_collection("leaves").find())
    
    for leave in leaves:
        leave["id"] = str(leave["_id"])
        del leave["_id"]
    
    return leaves

@router.put("/{leave_id}/{status}")
async def update_leave_status(leave_id: str, status: str):
    db = get_db()
    result = db.get_collection("leaves").update_one(
        {"_id": leave_id},
        {"$set": {"status": status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Leave not found")
    
    return {"message": "Leave status updated successfully"}
