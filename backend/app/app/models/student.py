from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Student(SQLModel, table=True):
    __tablename__ = "students"

    id: Optional[int] = Field(default=None, primary_key=True)
    student_no: str = Field(index=True, unique=True)
    name: str
    gender: Optional[str] = None
    class_id: Optional[int] = Field(default=None, foreign_key="classes.id")
    enroll_year: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
