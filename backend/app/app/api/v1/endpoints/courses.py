from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.api import deps
from app.core.response import ok
from app.models.course import Course
from app.models.teacher import Teacher
from app.schemas.edu_base import CourseCreate, CourseUpdate

router = APIRouter()


@router.post("/", status_code=201)
def create_course(
    payload: CourseCreate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    if payload.teacher_id is not None and session.get(Teacher, payload.teacher_id) is None:
        raise HTTPException(status_code=404, detail="teacher_not_found")
    record = Course(**payload.dict())
    session.add(record)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="duplicate_course_code")
    session.refresh(record)
    return ok(record.dict())


@router.get("/")
def list_courses(
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    rows = session.exec(select(Course)).all()
    return ok([item.dict() for item in rows])


@router.get("/{course_id}")
def get_course(
    course_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(Course, course_id)
    if row is None:
        raise HTTPException(status_code=404, detail="course_not_found")
    return ok(row.dict())


@router.put("/{course_id}")
def update_course(
    course_id: int,
    payload: CourseUpdate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(Course, course_id)
    if row is None:
        raise HTTPException(status_code=404, detail="course_not_found")
    updates = payload.dict(exclude_unset=True)
    teacher_id = updates.get("teacher_id")
    if teacher_id is not None and session.get(Teacher, teacher_id) is None:
        raise HTTPException(status_code=404, detail="teacher_not_found")
    for key, value in updates.items():
        setattr(row, key, value)
    session.add(row)
    session.commit()
    session.refresh(row)
    return ok(row.dict())


@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(Course, course_id)
    if row is None:
        raise HTTPException(status_code=404, detail="course_not_found")
    session.delete(row)
    session.commit()
    return ok(None)
