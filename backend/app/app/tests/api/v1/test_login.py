from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient

from app.core import config
from app.tests.utils.user import get_custom_user_token_headers


def test_get_access_token(client: TestClient, settings: config.Settings) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(settings.TOKEN_URL, data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_superuser_access_token(
    settings: config.Settings,
    client: TestClient,
    superuser_token_headers: Dict[str, str],
) -> None:
    r = client.post(
        settings.TOKEN_TEST_URL,
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_use_user_access_token(
    settings: config.Settings,
    client: TestClient,
    normal_user_token_headers: Dict[str, str],
) -> None:
    r = client.post(
        settings.TOKEN_TEST_URL,
        headers=normal_user_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_superuser_token_headers(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get("/test-current-active-superuser", headers=superuser_token_headers)
    user = r.json()
    assert r.status_code == 200
    assert user["email"] is not None
    assert user["is_superuser"] is True
    assert "role:admin" in user["scopes"]


def test_normal_user_token_headers(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get("/test-current-active-user", headers=normal_user_token_headers)
    user = r.json()
    assert r.status_code == 200
    assert user["email"] is not None
    assert "user:" + user["email"] in user["scopes"]


@pytest.fixture()
def custom_user_token_headers(
    client: TestClient, settings: config.Settings, collection: Any
) -> Dict[str, str]:
    return get_custom_user_token_headers(
        client, settings, collection, scopes=["role:custom"]
    )


def test_custom_user_token_headers(
    client: TestClient, custom_user_token_headers: Dict[str, str]
) -> None:
    r = client.get("/test-current-user", headers=custom_user_token_headers)
    user = r.json()
    assert r.status_code == 200
    assert user["email"] is not None
    assert "role:custom" in user["scopes"]


def test_superuser_permission_by_headers(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get("/test-user-permission", headers=superuser_token_headers)
    assert r.status_code == 200
    assert r.json() == {"status": "OK"}


def test_normal_user_permission_by_headers(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get("/test-user-permission", headers=normal_user_token_headers)
    assert r.status_code == 403
    assert r.json() == {"detail": "Insufficient permissions"}
