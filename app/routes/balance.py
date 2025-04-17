from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_session
from services.crud.balance import get_balance_by_user_id, deposit
from pydantic import BaseModel

balance_route = APIRouter()

class DepositRequest(BaseModel):
    user_id: int
    amount: float

@balance_route.get("/{user_id}")
def get_balance(user_id: int, session: Session = Depends(get_session)):
    try:
        balance = get_balance_by_user_id(session, user_id)
        if not balance:
            raise HTTPException(status_code=404, detail="Balance not found")
        return {"user_id": user_id, "balance": balance.amount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@balance_route.post("/deposit")
def deposit_balance(data: DepositRequest, session: Session = Depends(get_session)):
    try:
        balance = get_balance_by_user_id(session, data.user_id)
        if not balance:
            raise HTTPException(status_code=404, detail="Balance not found")
        updated_balance = deposit(session, balance.id, data.amount)
        return {"user_id": data.user_id, "balance": updated_balance.amount}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
