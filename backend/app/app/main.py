from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from sqlmodel import Session, select

from app.core import config
from app.core.config import settings
from app.core.exceptions import init_exception_handlers
from app.core.security import get_password_hash
from app.core.response import ok
from app.api.v1.api import router as v1_router
from app.api.v1.endpoints import auth, students, teachers, courses, classes, users
from app.db import sql_db
from app.models.user import User


def create_app(settings: config.Settings) -> FastAPI:
    app = FastAPI(root_path=settings.ROOT_STR, title="教务管理系统 API")

    # add it back if you are not using reverse-proxy
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=[
    #         "http://localhost:9528",
    #     ],
    #     allow_credentials=True,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )

    # instead of include_router, so to separate differnt versions
    app.include_router(v1_router)

    # compatibility aliases required by spec
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(students.router, prefix="/students", tags=["students"])
    app.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
    app.include_router(courses.router, prefix="/courses", tags=["courses"])
    app.include_router(classes.router, prefix="/classes", tags=["classes"])

    init_exception_handlers(app)

    @app.get("/status")
    def read_api_status() -> Dict[str, str]:
        return {"status": "OK"}

    @app.get("/health")
    def read_health() -> dict:
        return ok({"status": "ok", "version": "0.1.0"})

    return app


app = create_app(settings)


# in case it is needed
@app.on_event("startup")
def startup() -> None:
    sql_db.create_db_and_tables()
    with Session(sql_db.engine) as session:
        stmt = select(User).where(User.username == "admin")
        user = session.exec(stmt).first()
        if user is None:
            user = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role="admin",
                is_active=True,
            )
            session.add(user)
            session.commit()


#
#
# @app.on_event('shutdown')
# async def shutdown() -> None:
#    pass
