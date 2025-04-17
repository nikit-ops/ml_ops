from sqlmodel import SQLModel, Field, Relationship, Column, AutoString
from typing import Optional
from datetime import datetime

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    animal_type: "AnimalType" = Field(sa_column=Column(AutoString))
    confidence: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    task_id: int = Field(foreign_key="mltask.id")

    user: Optional["User"] = Relationship(back_populates="predictions")
    # task: Optional["MLTask"] = Relationship(back_populates="prediction")