import pytest
import httpx

from app.api.fastapi_users_utils import fastapi_users_instance

@pytest.mark.asyncio
async def test_superuser_token_headers(
    client: httpx.AsyncClient,
    superuser_token_headers
    ):
    r = await client.get('/test-user-permission', headers=superuser_token_headers)
    assert r.status_code == 200
    assert r.json() == {'status': 'OK'}



@pytest.mark.asyncio
async def test_normal_user_token_headers(
    client: httpx.AsyncClient,
    normal_user_token_headers
    ):
    r = await client.get('/test-user-permission', headers=normal_user_token_headers)
    assert r.status_code == 403
    assert r.json() == {'detail': 'Insufficient permissions'}
