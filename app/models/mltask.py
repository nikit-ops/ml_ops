from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from enum import Enum
from datetime import datetime

# if TYPE_CHECKING:
#     from .prediction import Prediction
#     from .user import User

class MLTaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class AnimalType(str, Enum):
    CAT = "cat"
    DOG = "dog"
    UNKNOWN = "unknown"

class MLTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_path: str
    cost: float = Field(default=10.0)
    status: MLTaskStatus = Field(default=MLTaskStatus.PENDING)
    result: Optional["AnimalType"] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

    # Relationships
    # user: Optional["User"] = Relationship(back_populates="tasks")
    # prediction: Optional["Prediction"] = Relationship(back_populates="task")