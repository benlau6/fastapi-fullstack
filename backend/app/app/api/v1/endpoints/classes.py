from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.api import deps
from app.core.response import ok
from app.models.class_model import ClassModel
from app.models.teacher import Teacher
from app.schemas.edu_base import ClassCreate, ClassUpdate

router = APIRouter()


@router.post("/", status_code=201)
def create_class(
    payload: ClassCreate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    if payload.head_teacher_id is not None and session.get(Teacher, payload.head_teacher_id) is None:
        raise HTTPException(status_code=404, detail="teacher_not_found")
    row = ClassModel(**payload.dict())
    session.add(row)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="duplicate_class_code")
    session.refresh(row)
    return ok(row.dict())


@router.get("/")
def list_classes(
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    rows = session.exec(select(ClassModel)).all()
    return ok([item.dict() for item in rows])


@router.get("/{class_id}")
def get_class(
    class_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(ClassModel, class_id)
    if row is None:
        raise HTTPException(status_code=404, detail="class_not_found")
    return ok(row.dict())


@router.put("/{class_id}")
def update_class(
    class_id: int,
    payload: ClassUpdate,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(ClassModel, class_id)
    if row is None:
        raise HTTPException(status_code=404, detail="class_not_found")
    updates = payload.dict(exclude_unset=True)
    teacher_id = updates.get("head_teacher_id")
    if teacher_id is not None and session.get(Teacher, teacher_id) is None:
        raise HTTPException(status_code=404, detail="teacher_not_found")
    for key, value in updates.items():
        setattr(row, key, value)
    session.add(row)
    session.commit()
    session.refresh(row)
    return ok(row.dict())


@router.delete("/{class_id}")
def delete_class(
    class_id: int,
    session: Session = Depends(deps.get_session),
    _: Any = Depends(deps.require_admin),
):
    row = session.get(ClassModel, class_id)
    if row is None:
        raise HTTPException(status_code=404, detail="class_not_found")
    session.delete(row)
    session.commit()
    return ok(None)
