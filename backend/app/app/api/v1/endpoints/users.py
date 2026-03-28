from typing import Any

from fastapi import APIRouter, Depends

from app.api import deps
from app.core.response import ok
from app.models.user import User

router = APIRouter()


@router.get("/me")
def read_user_me(current_user: User = Depends(deps.get_current_sql_user)) -> dict:
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


@router.get("/")
def list_users(_: Any = Depends(deps.require_admin)) -> dict:
    return ok([])
