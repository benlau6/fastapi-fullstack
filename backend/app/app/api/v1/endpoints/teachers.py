from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.api import deps
from app.core.response import ok
from app.models.teacher import Teacher
from app.models.course import Course
from app.schemas.edu_base import TeacherCreate, TeacherUpdate

router = APIRouter()


@router.post("/", status_code=201)
def create_teacher(
    payload: TeacherCreate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    record = Teacher(**payload.dict())
    session.add(record)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="duplicate_teacher_no")
    session.refresh(record)
    return ok(record.dict())


@router.get("/")
def list_teachers(
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    rows = session.exec(select(Teacher)).all()
    return ok([item.dict() for item in rows])


@router.get("/{teacher_id}")
def get_teacher(
    teacher_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(Teacher, teacher_id)
    if row is None:
        raise HTTPException(status_code=404, detail="teacher_not_found")
    return ok(row.dict())


@router.put("/{teacher_id}")
def update_teacher(
    teacher_id: int,
    payload: TeacherUpdate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(Teacher, teacher_id)
    if row is None:
        raise HTTPException(status_code=404, detail="teacher_not_found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(row, key, value)
    session.add(row)
    session.commit()
    session.refresh(row)
    return ok(row.dict())


@router.delete("/{teacher_id}")
def delete_teacher(
    teacher_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(Teacher, teacher_id)
    if row is None:
        raise HTTPException(status_code=404, detail="teacher_not_found")
    in_use = session.exec(select(Course).where(Course.teacher_id == teacher_id)).first()
    if in_use is not None:
        raise HTTPException(status_code=409, detail="resource_in_use")
    session.delete(row)
    session.commit()
    return ok(None)
