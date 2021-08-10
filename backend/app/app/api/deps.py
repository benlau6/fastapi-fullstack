from functools import lru_cache
from typing import AsyncGenerator

from fastapi import Header, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from jose import jwt
from fastapi_permissions import configure_permissions
from fastapi_permissions import Authenticated, Everyone

from app import models, schemas, crud
from app.core import config, security
from app.core.config import settings # immutable
from app.db.session import AsyncSessionLocal



############# settings ###########
@lru_cache
def get_settings():
    return config.Settings()


# Dependency
async def get_db() -> AsyncGenerator:
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        db.close()


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

    
##################################
# could be used for fine-grained control
async def verify_content_length(content_length: int = Header(...)):
    if content_length > settings.PAYLOAD_LIMIT:
        raise HTTPException(status_code=413, detail=f"Error, please make sure the files are smaller than {settings.PAYLOAD_LIMIT}")


async def verify_content_type(content_type: int = Header(...)):
    accepted_types = ['csv', 'png']
    if content_type not in accepted_types:
        raise HTTPException(status_code=..., detail=f"Incorrect file type")


async def verify_key(x_api_key: str = Header(...)):
    if x_api_key != "key":
        raise HTTPException(status_code=400, detail="X-Api-Key header invalid")


############ fastapi-users #############
def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_user_principals(current_user: schemas.User = Depends(get_current_active_user)):
    if current_user is not None:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.extend(getattr(current_user, "principals", []))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals

# Permission is already wrapped in Depends()
Permission = configure_permissions(get_current_active_user_principals)