from typing import Dict, List

import pytest
from async_asgi_testclient import TestClient

from app import crud
from app.core import config
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

def create_random_user(db) -> dict:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    return user


@pytest.mark.asyncio
async def user_authentication_headers(
    *, client: TestClient, settings: config.Settings, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}
    r = await client.post(settings.TOKEN_URL, form=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


@pytest.mark.asyncio
async def authentication_token_from_email(
    *, client: TestClient, settings: config.Settings, db, email: str
) -> Dict[str, str]:
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = await crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = await crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = await crud.user.update(db, db_obj=user, obj_in=user_in_update)

    return await user_authentication_headers(client=client, settings=settings, email=email, password=password)