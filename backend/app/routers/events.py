from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date, datetime
from pydantic import BaseModel
from backend.core.database import get_db

router = APIRouter()

class Event(BaseModel):
    title: str
    description: str
    event_date: date
    event_time: str
    location: str
    organizer: str
    event_type: str = "College Event"

class EventResponse(BaseModel):
    id: str
    title: str
    description: str
    event_date: date
    event_time: str
    location: str
    organizer: str
    event_type: str
    created_at: datetime

@router.post("/", response_model=EventResponse)
async def create_event(event: Event):
    db = get_db()
    event_data = event.dict()
    event_data["created_at"] = datetime.now()
    
    result = db.get_collection("events").insert_one(event_data)
    event_data["id"] = str(result.inserted_id)
    
    return event_data

@router.get("/", response_model=List[EventResponse])
async def get_events(event_type: str = None):
    db = get_db()
    query = {}
    
    if event_type:
        query["event_type"] = event_type
    
    events = list(db.get_collection("events").find(query).sort("event_date", 1))
    
    for event in events:
        event["id"] = str(event["_id"])
        del event["_id"]
    
    return events

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    db = get_db()
    event = db.get_collection("events").find_one({"_id": event_id})
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event["id"] = str(event["_id"])
    del event["_id"]
    
    return event

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    db = get_db()
    result = db.get_collection("events").delete_one({"_id": event_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {"message": "Event deleted successfully"}
