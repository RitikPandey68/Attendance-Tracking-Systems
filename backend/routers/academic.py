from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
import uuid
from models.academic import *
from core.database import get_database
from routers.auth import get_current_user

router = APIRouter(prefix="/academic", tags=["academic"])

@router.post("/notes", response_model=Note)
async def create_note(
    note: NoteCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["faculty", "admin"]:
        raise HTTPException(status_code=403, detail="Only faculty and admin can create notes")
    
    note_data = note.dict()
    note_data["id"] = str(uuid.uuid4())
    note_data["faculty_id"] = current_user["id"]
    note_data["created_at"] = datetime.now()
    note_data["updated_at"] = datetime.now()
    
    db.notes.insert_one(note_data)
    return Note(**note_data)

@router.get("/notes", response_model=List[Note])
async def get_notes(
    subject: Optional[str] = None,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    query = {}
    if subject:
        query["subject"] = subject
    
    notes = list(db.notes.find(query))
    return [Note(**note) for note in notes]