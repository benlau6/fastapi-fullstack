from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.api import deps
from app.core.config import settings
from app.core.response import ok
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.edu_base import LoginIn

router = APIRouter()


def _build_token_response(user: User) -> dict:
    expires_in = 60
    token = create_access_token(
        data={"sub": str(user.id), "scopes": ["role:admin"]},
        expires_delta=timedelta(minutes=expires_in),
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expires_in * 60,
    }


@router.post("/login/access-token")
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session),
) -> dict:
    stmt = select(User).where(User.username == form_data.username)
    user = session.exec(stmt).first()
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid_credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="inactive_user")
    return ok(_build_token_response(user))


@router.post("/login")
def login_json(payload: LoginIn, session: Session = Depends(deps.get_session)) -> dict:
    stmt = select(User).where(User.username == payload.username)
    user = session.exec(stmt).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid_credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="inactive_user")
    return ok(_build_token_response(user))


@router.get("/me")
def read_me(current_user: User = Depends(deps.get_current_sql_user)) -> dict:
    return ok(
        {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at,
            "scopes": ["role:admin"],
        }
    )


@router.post("/logout")
def logout() -> dict:
    return ok({"msg": "logout_ok"})
