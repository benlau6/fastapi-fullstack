from sqlmodel import SQLModel, create_engine

from app.core.config import settings


# by ensuring you don't share the same session with more than one request, the code is already safe.
# need to disable it because in FastAPI each request could be handled by multiple interacting threads.
connect_args = {"check_same_thread": False}
engine = create_engine(settings.SQLITE_URI, echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
