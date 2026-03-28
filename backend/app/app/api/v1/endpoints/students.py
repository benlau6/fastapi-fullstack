from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.api import deps
from app.core.response import ok
from app.models.student import Student
from app.schemas.edu_base import StudentCreate, StudentUpdate

router = APIRouter()


@router.post("/", status_code=201)
def create_student(
    payload: StudentCreate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    student = Student(**payload.dict())
    session.add(student)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="duplicate_student_no")
    session.refresh(student)
    return ok(student.dict())


@router.get("/")
def list_students(
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    records = session.exec(select(Student)).all()
    return ok([item.dict() for item in records])


@router.get("/{student_id}")
def get_student(
    student_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    record = session.get(Student, student_id)
    if record is None:
        raise HTTPException(status_code=404, detail="student_not_found")
    return ok(record.dict())


@router.put("/{student_id}")
def update_student(
    student_id: int,
    payload: StudentUpdate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    record = session.get(Student, student_id)
    if record is None:
        raise HTTPException(status_code=404, detail="student_not_found")
    updates = payload.dict(exclude_unset=True)
    for key, value in updates.items():
        setattr(record, key, value)
    session.add(record)
    session.commit()
    session.refresh(record)
    return ok(record.dict())


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    record = session.get(Student, student_id)
    if record is None:
        raise HTTPException(status_code=404, detail="student_not_found")
    session.delete(record)
    session.commit()
    return ok(None)
