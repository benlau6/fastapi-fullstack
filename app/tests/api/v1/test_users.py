from typing import Dict

import pytest
from async_asgi_testclient import TestClient

from app import crud
from app.core import config
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

# https://fastapi.tiangolo.com/tutorial/testing/

@pytest.mark.asyncio
async def test_get_users_superuser_me(
    client: TestClient, settings: config.Settings, superuser_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.asyncio
async def test_get_users_normal_user_me(
    client: TestClient, settings: config.Settings, normal_user_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER
#
#
#def test_create_user_new_email(
#    client: TestClient, settings: config.Settings,superuser_token_headers: dict, collection
#) -> None:
#    username = random_email()
#    password = random_lower_string()
#    data = {"email": username, "password": password}
#    r = client.post(
#        f"{settings.ROOT_STR}{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
#    )
#    assert 200 <= r.status_code < 300
#    created_user = r.json()
#    user = crud.user.get_by_email(collection, email=username)
#    assert user
#    assert user['email'] == created_user["email"]
#    assert 'hashed_password' not in created_user
#    assert 'password' not in created_user
#
#
#def test_get_existing_user(
#    client: TestClient, settings: config.Settings, superuser_token_headers: dict, collection
#) -> None:
#    username = random_email()
#    password = random_lower_string()
#    user_in = UserCreate(email=username, password=password)
#    user = crud.user.create(collection, document_in=user_in)
#    user_id = user['_id']
#    r = client.get(
#        f"{settings.ROOT_STR}{settings.API_V1_STR}/users/{str(user_id)}", headers=superuser_token_headers,
#    )
#    assert 200 <= r.status_code < 300
#    api_user = r.json()
#    existing_user = crud.user.get_by_email(collection, email=username)
#    assert existing_user
#    assert existing_user['email'] == api_user["email"]
#    assert 'hashed_password' not in api_user
#    assert 'password' not in api_user
#
#
#def test_create_user_existing_username(
#    client: TestClient, settings: config.Settings, superuser_token_headers: dict, collection
#) -> None:
#    username = random_email()
#    # username = email
#    password = random_lower_string()
#    user_in = UserCreate(email=username, password=password)
#    crud.user.create(collection, document_in=user_in)
#    data = {"email": username, "password": password}
#    r = client.post(
#        f"{settings.ROOT_STR}{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
#    )
#    created_user = r.json()
#    assert r.status_code == 400
#    assert "_id" not in created_user
#    assert 'hashed_password' not in created_user
#    assert 'password' not in created_user
#
#
#def test_create_user_by_normal_user(
#    client: TestClient, settings: config.Settings, normal_user_token_headers: Dict[str, str]
#) -> None:
#    username = random_email()
#    password = random_lower_string()
#    data = {"email": username, "password": password}
#    r = client.post(
#        f"{settings.ROOT_STR}{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
#    )
#    created_user = r.json()
#    assert r.status_code == 400
#    assert 'hashed_password' not in created_user
#    assert 'password' not in created_user
#
#
#def test_retrieve_users(
#    client: TestClient, settings: config.Settings, superuser_token_headers: dict, collection
#) -> None:
#    username = random_email()
#    password = random_lower_string()
#    user_in = UserCreate(email=username, password=password)
#    crud.user.create(collection, document_in=user_in)
#
#    username2 = random_email()
#    password2 = random_lower_string()
#    user_in2 = UserCreate(email=username2, password=password2)
#    crud.user.create(collection, document_in=user_in2)
#
#    r = client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/users/", headers=superuser_token_headers)
#    all_users = r.json()
#
#    assert len(all_users) > 1
#    for item in all_users:
#        assert "email" in item
#        assert 'hashed_password' not in item
#        assert 'password' not in item
