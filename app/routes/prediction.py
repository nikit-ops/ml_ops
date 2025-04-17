from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import get_session
from services.crud.mltask import create_task_for_user_with_prediction
from models.mlmodel import MlModel
from pydantic import BaseModel

prediction_route = APIRouter()

class PredictionRequest(BaseModel):
    user_id: int
    image_path: str
    cost: float

@prediction_route.post("/")
def predict(data: PredictionRequest, session: Session = Depends(get_session)):
    try:
        model = session.query(MlModel).first()
        if not model:
            raise HTTPException(status_code=404, detail="Prediction model not found")
        task = create_task_for_user_with_prediction(
            session, data.user_id, data.image_path, data.cost, model=model
        )
        return {"task_id": task.id, "status": task.status, "prediction": task.result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
