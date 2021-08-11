import pytest
from fastapi.testclient import TestClient


def test_superuser_token_headers(
    client: TestClient,
    superuser_token_headers
    ):
    r = client.get('/test-user-permission', headers=superuser_token_headers)
    assert r.status_code == 200
    assert r.json() == {'status': 'OK'}



def test_normal_user_token_headers(
    client: TestClient,
    normal_user_token_headers
    ):
    r = client.get('/test-user-permission', headers=normal_user_token_headers)
    assert r.status_code == 403
    assert r.json() == {'detail': 'Insufficient permissions'}
