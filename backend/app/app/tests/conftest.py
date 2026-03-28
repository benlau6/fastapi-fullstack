from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    response = client.post(
        "/v1/auth/login/access-token",
        data={"username": "admin", "password": "admin123"},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def normal_user_token_headers(client: TestClient) -> Dict[str, str]:
    response = client.post(
        "/v1/auth/login/access-token",
        data={"username": "admin", "password": "admin123"},
    )
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
