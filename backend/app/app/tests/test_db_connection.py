from sqlalchemy import text
from sqlmodel import Session

from app.db.sql_db import engine


def test_sqlite_engine_works():
    with Session(engine) as session:
        row = session.exec(text("SELECT 1")).one()
    assert row[0] == 1
