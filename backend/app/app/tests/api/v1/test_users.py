from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from app import crud, schemas
from app.core import config
from app.tests.utils.utils import random_email, random_lower_string


# https://fastapi.tiangolo.com/tutorial/testing/
def test_get_users_superuser_me(
    client: TestClient,
    settings: config.Settings,
    superuser_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.USERS_URL}/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(
    client: TestClient,
    settings: config.Settings,
    normal_user_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.USERS_URL}/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.FIRST_NORMAL_USER


def test_get_existing_user(
    client: TestClient,
    settings: config.Settings,
    collection: Any,
    superuser_token_headers: Dict[str, str],
) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user_id = crud.user.create(collection, document_in=user_in)
    r = client.get(
        f"{settings.USERS_URL}/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    found_user = r.json()
    assert found_user
    assert found_user["email"] == email


# def test_register(
#    client: TestClient, settings: config.Settings
# ) -> None:
#    username = random_email()
#    password = random_lower_string()
#    register_data = {"email": username, "password": password}
#    r = client.post(
#        f'{settings.AUTH_URL}/register', json=register_data, #or data if already jsonalized
#    )
#    assert r.status_code == 201
#    created_user = r.json()
#    assert created_user['principals'] == [f'user:{username}']
#    assert 'hashed_password' not in created_user
#    assert 'password' not in created_user
