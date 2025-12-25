from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, date
import uuid
from models.academic import FeeDetail, FeeDetailCreate, FeePayment, FeePaymentCreate, FeeType
from core.database import get_database
from routers.auth import get_current_user

router = APIRouter(prefix="/fees", tags=["fees"])

@router.post("/", response_model=FeeDetail)
async def create_fee_detail(
    fee: FeeDetailCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    if current_user["role"] not in ["admin", "finance_admin"]:
        raise HTTPException(status_code=403, detail="Only admin can create fee details")
    
    fee_data = fee.dict()
    fee_data["id"] = str(uuid.uuid4())
    fee_data["created_at"] = datetime.now()
    fee_data["updated_at"] = datetime.now()
    
    db.fee_details.insert_one(fee_data)
    return FeeDetail(**fee_data)

@router.get("/student/{student_id}", response_model=List[FeeDetail])
async def get_student_fees(
    student_id: str,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    # Students can only view their own fees
    if current_user["role"] == "student" and current_user["id"] != student_id:
        raise HTTPException(status_code=403, detail="Can only view your own fees")
    
    fees = list(db.fee_details.find({"student_id": student_id}).sort("due_date", 1))
    return [FeeDetail(**fee) for fee in fees]