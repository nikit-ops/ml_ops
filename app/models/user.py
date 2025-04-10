from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from models.balance import Balance

if TYPE_CHECKING:
    from models.transaction import Transaction
    from .prediction import Prediction

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    is_admin: bool = Field(default=False)

    # Relationship to balance
    balance: Optional["Balance"] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})

    # Relationship to transactions
    transactions: List["Transaction"] = Relationship(back_populates="user")

    # Relationship to predictions
    predictions: List["Prediction"] = Relationship(back_populates="user")
