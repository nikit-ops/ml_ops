from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_session
from services.crud.transaction import get_transaction_history_by_user_id
from database.redis_client import redis_client  

transaction_route = APIRouter()

@transaction_route.get("/{user_id}")
def get_transactions(
    user_id: int,
    session: Session = Depends(get_session),
    token: str = None  
):
    try:
        
        if not token:
            raise HTTPException(status_code=401, detail="Token is required")
        
        user_id_from_token = redis_client.get(f"auth_token:{token}")
        if not user_id_from_token:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        
        if int(user_id_from_token) != user_id:
            raise HTTPException(status_code=403, detail="Access forbidden")

        transactions = get_transaction_history_by_user_id(session, user_id)
        return [
            {
                "transaction_id": t.id,
                "type": t.type,
                "amount": t.amount,
                "timestamp": t.timestamp,
            }
            for t in transactions
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
