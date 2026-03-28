from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_code: str = Field(index=True, unique=True)
    course_name: str
    credit: Optional[float] = None
    teacher_id: Optional[int] = Field(default=None, foreign_key="teachers.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
