from typing import Any, List

from fastapi import APIRouter

from app import schemas, models


router = APIRouter()


@router.get("", response_model=List[schemas.User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    return await models.UserModel.all().offset(skip).limit(limit)