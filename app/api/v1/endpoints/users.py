from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr

from app import crud, schemas
from app.api import deps
from app.core.config import settings


router = APIRouter()


#@router.get("/", response_model=List[schemas.User])
#def read_users(
#    skip: int = 0,
#    limit: int = 100,
#    current_user: schemas.User = Depends(deps.get_current_active_superuser),
#    collection = Depends(deps.get_user_collection),
#) -> Any:
#    """
#    Retrieve users.
#    """
#    users = crud.user.get_multi(collection, skip=skip, limit=limit)
#    return users
