from functools import lru_cache

from fastapi import (
    Header,
    Body,
    Depends, 
    Security,
    HTTPException, 
    status, 
)
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi_permissions import configure_permissions
from fastapi_permissions import Authenticated, Everyone
from pydantic import ValidationError
from jose import jwt

from app import schemas, crud
from app.core import security, config
from app.core.config import settings
from app.db.mongo import client


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


############# settings ###########
@lru_cache
def get_settings() -> config.Settings:
    return config.Settings()


def get_db(settings: config.Settings = Depends(get_settings)):
    return client[settings.MONGO_DB_NAME]


def get_user_collection(db = Depends(get_db)):
    return db.user
    

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


############ user #############
def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    collection = Depends(get_user_collection),
) -> schemas.User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        _id: str = payload.get('sub')
        if _id is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        token_data = schemas.TokenData(scopes=token_scopes, id=_id)
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    user = crud.user.get(collection, id=token_data.id)
    if user is None:
        raise credentials_exception
    if not crud.user.is_superuser(user):
        for scope in security_scopes.scopes:
            if scope not in token_data.scopes:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": authenticate_value},
                )
    return user


def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
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
ActiveUserPermission = configure_permissions(get_current_active_user_principals)