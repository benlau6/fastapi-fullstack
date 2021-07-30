from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app import schemas, models
from app.api import deps
from app.core.config import settings


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