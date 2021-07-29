from typing import Dict

import pytest
import httpx

from app.core import config
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

# https://fastapi.tiangolo.com/tutorial/testing/

@pytest.mark.asyncio
async def test_get_users_superuser_me(
    client: httpx.AsyncClient, settings: config.Settings, superuser_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.USERS_URL}/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.asyncio
async def test_get_users_normal_user_me(
    client: httpx.AsyncClient, settings: config.Settings, normal_user_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.USERS_URL}/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


#@pytest.mark.asyncio
#async def test_get_existing_user(
#    client: httpx.AsyncClient, settings: config.Settings, mock_fastapi_users_instance, superuser_token_headers: dict, db
#) -> None:
#    username = random_email()
#    password = random_lower_string()
#    user_in = UserCreate(email=username, password=password)
#    user = await mock_fastapi_users_instance.create(obj_in=user_in)
#    user_id = user.id
#    r = await client.get(
#        f"{settings.USERS_URL}/{user_id}", headers=superuser_token_headers,
#    )
#    assert 200 <= r.status_code < 300
#    api_user = r.json()
#    existing_user = await mock_fastapi_users_instance.get_user(username)
#    assert existing_user
#    assert existing_user.email == api_user["email"]
#    assert 'hashed_password' not in api_user
#    assert 'password' not in api_user
#
#
#@pytest.mark.asyncio
#async def test_register(
#    client: httpx.AsyncClient, settings: config.Settings, normal_user_token_headers: Dict[str, str]
#) -> None:
#    username = random_email()
#    password = random_lower_string()
#    data = {"email": username, "password": password}
#    r = await client.post(
#        f'{settings.AUTH_URL}/register', headers=normal_user_token_headers, json=data,
#    )
#    created_user = r.json()
#    assert r.status_code == 201
#    assert 'hashed_password' not in created_user
#    assert 'password' not in created_user
