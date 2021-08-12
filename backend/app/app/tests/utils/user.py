from typing import Dict, List

import pytest
from fastapi.testclient import TestClient

from app import schemas, crud
from app.core import config
from app.tests.utils.utils import random_email, random_lower_string


@pytest.fixture
def principals():
    return ["role:test"]


def get_superuser_token_headers(
    client: TestClient, settings: config.Settings
) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(settings.TOKEN_URL, data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_normal_user_token_headers(
    client: TestClient, settings: config.Settings,
) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_NORMAL_USER,
        "password": settings.FIRST_NORMAL_USER_PASSWORD,
    }
    r = client.post(settings.TOKEN_URL, data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_custom_user_token_headers(
    client: TestClient, settings: config.Settings, collection, *, scopes: List[str],
) -> Dict[str, str]:
    email = random_email()
    password = random_lower_string()
    obj_in = schemas.UserCreate(
        email=email, password=password, scopes=["user:" + email] + scopes
    )
    crud.user.create(collection, obj_in)
    login_data = {"username": email, "password": password}
    r = client.post(settings.TOKEN_URL, data=login_data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
