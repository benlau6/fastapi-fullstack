from typing import Dict, List

import pytest
import httpx

from app import schemas
from app.core import config
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
from app.api.fastapi_users_utils import fastapi_users_instance


@pytest.fixture
def principals():
    return ['role:test']


@pytest.mark.asyncio
async def get_superuser_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    superuser
    ) -> Dict[str, str]:
    login_data = {"username": superuser.email, "password": 'password',}
    r = await client.post(settings.TOKEN_URL, data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.mark.asyncio
async def get_normal_user_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    user,
    ) -> Dict[str, str]:
    login_data = {"username": user.email, "password": 'password'}
    r = await client.post(settings.TOKEN_URL, data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.mark.asyncio
async def get_custom_user_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    principals: List[str]
) -> Dict[str, str]:
    email=random_email()
    password=random_lower_string()
    obj_in = schemas.UserCreate(
        email=email,
        password=password,
        principals=['user:'+email] + principals
    )
    await fastapi_users_instance.create_user(obj_in)
    login_data = {"username": email, "password": password}
    r = await client.post(settings.TOKEN_URL, data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
