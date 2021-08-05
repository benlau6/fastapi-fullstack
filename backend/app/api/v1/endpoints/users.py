from typing import Any, List

from fastapi import APIRouter, Depends

from app import schemas, models
from app.api import deps


router = APIRouter()


@router.get(
    "", 
    response_model=List[schemas.User], 
    dependencies=[Depends(deps.get_current_active_superuser)])
async def get_users(
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    return await models.UserModel.all().offset(skip).limit(limit)