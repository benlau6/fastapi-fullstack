from typing import Dict

import pytest
from fastapi.testclient import TestClient

from app.core import config
from app.tests.utils.user import get_custom_user_token_headers


def test_get_superuser_token_headers(
    client: TestClient, 
    settings: config.Settings, 
    superuser
    ) -> Dict[str, str]:
    login_data = {"username": settings.FIRST_SUPERUSER, "password": settings.FIRST_SUPERUSER_PASSWORD}
    r = client.post(settings.TOKEN_URL, data=login_data)
    response = r.json()
    assert settings.TOKEN_URL == 1
    assert response == 1
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}", 'path':settings.TOKEN_URL}


def test_superuser_token_headers(
    client: TestClient,
    superuser_token_headers
    ):
    r = client.get('/test-current-active-superuser', headers=superuser_token_headers)
    user = r.json()
    assert user == 1
    assert r.status_code == 200
    assert user['email'] is not None
    assert user['is_superuser'] == True
    assert 'role:admin' in user['principals']


def test_normal_user_token_headers(
    client: TestClient,
    normal_user_token_headers
    ):
    r = client.get('/test-current-active-user', headers=normal_user_token_headers)
    user = r.json()
    assert user == 1
    assert r.status_code == 200
    assert user['email'] is not None
    assert user['is_verified'] == True
    assert 'user:'+user['email'] in user['principals']  


@pytest.fixture()
def custom_user_token_headers(
    client: TestClient, 
    settings: config.Settings, 
    ) -> Dict[str, str]:
    return get_custom_user_token_headers(client, settings, principals=['role:custom'])


def test_custom_user_token_headers(
    client: TestClient, 
    custom_user_token_headers
    ) -> Dict[str, str]:
    r = client.get('/test-current-user', headers=custom_user_token_headers)
    user = r.json()
    assert r.status_code == 200
    assert user['email'] is not None
    assert 'role:custom' in user['principals']