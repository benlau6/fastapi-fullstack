from typing import Dict

import pytest
import httpx

from app.core import config
from app.tests.utils.user import get_custom_user_token_headers

@pytest.mark.asyncio
async def test_superuser_token_headers(
    client: httpx.AsyncClient,
    superuser_token_headers
    ):
    r = await client.get('/test-current-superuser', headers=superuser_token_headers)
    user = r.json()
    assert r.status_code == 200
    assert user['email'] is not None
    assert user['is_superuser'] == True
    assert 'role:admin' in user['principals']


@pytest.mark.asyncio
async def test_normal_user_token_headers(
    client: httpx.AsyncClient,
    normal_user_token_headers
    ):
    r = await client.get('/test-current-user', headers=normal_user_token_headers)
    user = r.json()
    assert r.status_code == 200
    assert user['email'] is not None
    assert user['is_verified'] == True
    assert 'user:'+user['email'] in user['principals']  


@pytest.fixture()
async def custom_user_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    ) -> Dict[str, str]:
    return await get_custom_user_token_headers(client, settings, principals=['role:custom'])


@pytest.mark.asyncio
async def test_custom_user_token_headers(
    client: httpx.AsyncClient, 
    custom_user_token_headers
    ) -> Dict[str, str]:
    r = await client.get('/test-current-user', headers=custom_user_token_headers)
    user = r.json()
    assert r.status_code == 200
    assert user['email'] is not None
    assert 'role:custom' in user['principals']