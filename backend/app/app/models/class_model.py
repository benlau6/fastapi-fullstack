from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ClassModel(SQLModel, table=True):
    __tablename__ = "classes"

    id: Optional[int] = Field(default=None, primary_key=True)
    class_code: str = Field(index=True, unique=True)
    class_name: str
    grade: str
    head_teacher_id: Optional[int] = Field(default=None, foreign_key="teachers.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
