import pytest
import httpx

from app.core import config
from app.api.fastapi_users_utils import fastapi_users_instance

@pytest.mark.asyncio
async def test_superuser_token_headers(
    client,
    superuser_token_headers
    ):
    r = await client.get('/test-current-superuser', headers=superuser_token_headers)
    user = r.json()
    assert user
    assert user['is_superuser'] == True


@pytest.mark.asyncio
async def test_normal_user_token_headers(
    client,
    normal_user_token_headers
    ):
    r = await client.get('/test-current-user', headers=normal_user_token_headers)
    user = r.json()
    assert user
    assert user['is_verified'] == True
