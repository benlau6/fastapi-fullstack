from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Envelope(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


class LoginIn(BaseModel):
    username: str
    password: str


class AuthPayload(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class CurrentUserOut(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool
    created_at: datetime


class StudentBase(BaseModel):
    student_no: str
    name: str
    gender: Optional[str] = None
    class_id: Optional[int] = None
    enroll_year: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    class_id: Optional[int] = None
    enroll_year: Optional[int] = None


class TeacherBase(BaseModel):
    teacher_no: str
    name: str
    phone: Optional[str] = None


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


class CourseBase(BaseModel):
    course_code: str
    course_name: str
    credit: Optional[float] = None
    teacher_id: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    credit: Optional[float] = None
    teacher_id: Optional[int] = None


class ClassBase(BaseModel):
    class_code: str
    class_name: str
    grade: str
    head_teacher_id: Optional[int] = None


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    class_name: Optional[str] = None
    grade: Optional[str] = None
    head_teacher_id: Optional[int] = None
