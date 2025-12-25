from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date
from pydantic import BaseModel
from backend.core.database import get_db

router = APIRouter()

class Holiday(BaseModel):
    date: date
    name: str
    description: str
    state: str = "All"
    type: str = "Government"

class HolidayResponse(BaseModel):
    id: str
    date: date
    name: str
    description: str
    state: str
    type: str

@router.post("/", response_model=HolidayResponse)
async def add_holiday(holiday: Holiday):
    db = get_db()
    holiday_data = holiday.dict()
    
    result = db.get_collection("holidays").insert_one(holiday_data)
    holiday_data["id"] = str(result.inserted_id)
    
    return holiday_data

@router.get("/", response_model=List[HolidayResponse])
async def get_holidays(state: str = None, holiday_type: str = None):
    db = get_db()
    query = {}
    
    if state:
        query["state"] = state
    if holiday_type:
        query["type"] = holiday_type
    
    holidays = list(db.get_collection("holidays").find(query))
    
    for holiday in holidays:
        holiday["id"] = str(holiday["_id"])
        del holiday["_id"]
    
    return holidays

@router.get("/{holiday_id}", response_model=HolidayResponse)
async def get_holiday(holiday_id: str):
    db = get_db()
    holiday = db.get_collection("holidays").find_one({"_id": holiday_id})
    
    if not holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")
    
    holiday["id"] = str(holiday["_id"])
    del holiday["_id"]
    
    return holiday

@router.delete("/{holiday_id}")
async def delete_holiday(holiday_id: str):
    db = get_db()
    result = db.get_collection("holidays").delete_one({"_id": holiday_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Holiday not found")
    
    return {"message": "Holiday deleted successfully"}
