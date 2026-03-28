from fastapi import Depends, HTTPException

from app.main import app
from app.api import deps


def test_auth_me_requires_token(client):
    r = client.get("/v1/users/me")
    assert r.status_code == 401


def test_auth_login_success_returns_token(client):
    r = client.post(
        "/v1/auth/login/access-token",
        data={"username": "admin", "password": "admin123"},
    )
    assert r.status_code == 200
    assert "access_token" in r.json()["data"]


def test_spec_alias_login_works(client):
    r = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200


def test_spec_alias_me_works(client, superuser_token_headers):
    r = client.get("/auth/me", headers=superuser_token_headers)
    assert r.status_code == 200


def test_non_admin_forbidden(client, superuser_token_headers):
    def deny_admin():
        raise HTTPException(status_code=403, detail="forbidden")

    app.dependency_overrides[deps.require_admin] = deny_admin
    try:
        r = client.get("/v1/students", headers=superuser_token_headers)
        assert r.status_code == 403
    finally:
        app.dependency_overrides.pop(deps.require_admin, None)
