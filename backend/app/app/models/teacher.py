from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Teacher(SQLModel, table=True):
    __tablename__ = "teachers"

    id: Optional[int] = Field(default=None, primary_key=True)
    teacher_no: str = Field(index=True, unique=True)
    name: str
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
