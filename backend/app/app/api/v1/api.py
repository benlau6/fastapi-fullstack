from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    heroes,
    teams,
    students,
    teachers,
    courses,
    classes,
)

router = APIRouter(prefix="/v1")

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(heroes.router, prefix="/heroes", tags=["heroes"])
router.include_router(teams.router, prefix="/teams", tags=["teams"])
router.include_router(students.router, prefix="/students", tags=["students"])
router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
router.include_router(courses.router, prefix="/courses", tags=["courses"])
router.include_router(classes.router, prefix="/classes", tags=["classes"])
