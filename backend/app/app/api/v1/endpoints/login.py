from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
#from app.utils import (
#    generate_password_reset_token,
#    send_reset_password_email,
#    verify_password_reset_token,
#)

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
def login_for_access_token(
    collection = Depends(deps.get_user_collection), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        collection, email=form_data.username, password=form_data.password
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
            data={'sub': str(user['_id']), 'scopes': user['scopes']}, 
            expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/test-token", response_model=schemas.UserFromDB)
def test_token(current_user: schemas.UserFromDB = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user
