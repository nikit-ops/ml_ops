from sqlalchemy.orm import Session
from sqlalchemy import select
from models.transaction import Transaction
from typing import List


def get_transaction_history_by_user_id(
    session: Session, user_id: int
) -> List[Transaction]:
    """Retrieve the transaction history for a specific user by user_id."""
    statement = (
        select(Transaction)
        .where(Transaction.user_id == user_id)
        .order_by(Transaction.timestamp.desc())
    )
    result = session.execute(statement).scalars().all()
    return result
