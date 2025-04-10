from sqlalchemy.orm import Session
from models.mltask import MLTask, MLTaskStatus, AnimalType
from models.transaction import Transaction, TransactionType
from models.balance import Balance
from services.crud.balance import get_balance_by_user_id
from services.crud.prediction import get_prediction_from_model
from typing import Optional
import random
from models.mlmodel import MlModel


def create_mltask_for_user(
    session: Session, user_id: int, image_path: str, cost: float
) -> Optional[MLTask]:
    """Create an MLTask for a user and deduct the cost from their balance."""
    balance = get_balance_by_user_id(session, user_id)
    if not balance:
        raise ValueError(f"Balance for user_id {user_id} not found.")

    if balance.amount < cost:
        raise ValueError("Insufficient funds to create MLTask.")

    balance.amount -= cost
    session.add(balance)
    session.commit()

    transaction = Transaction(
        user_id=user_id,
        amount=-cost,
        type=TransactionType.PREDICTION_PAYMENT,
        description="MLTask creation cost",
    )
    session.add(transaction)
    session.commit()

    mltask = MLTask(
        user_id=user_id,
        image_path=image_path,
        cost=cost,
        status=MLTaskStatus.PENDING,
    )
    session.add(mltask)
    session.commit()
    session.refresh(mltask)

    return mltask


def create_task_for_user_with_prediction(
    session: Session, user_id: int, image_path: str, cost: float, model: MlModel
) -> MLTask:
    """Create a task for a user, deduct the cost, and generate a prediction."""
    task = create_mltask_for_user(session, user_id, image_path, cost)
    try:
        prediction = get_prediction_from_model(model, image_path)
        task.result = prediction
        task.status = MLTaskStatus.COMPLETED
    except Exception as e:
        task.status = MLTaskStatus.FAILED
        task.result = None 
        print(f"Prediction failed: {e}")
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


