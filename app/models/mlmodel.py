from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    pass

class MlModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = ""