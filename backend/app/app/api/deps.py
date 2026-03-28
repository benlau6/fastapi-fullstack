from functools import lru_cache
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlmodel import Session

from app.core import config, security
from app.core.config import settings
from app.db.sql_db import engine
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


@lru_cache
def get_settings() -> config.Settings:
    return config.Settings()


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


def get_current_sql_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        user_id = int(sub)
    except Exception:
        raise credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user


def require_admin(current_user: User = Depends(get_current_sql_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="inactive_user")
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="forbidden")
    return current_user
