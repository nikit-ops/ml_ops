from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = Field(default=0.0)
    
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="balance")