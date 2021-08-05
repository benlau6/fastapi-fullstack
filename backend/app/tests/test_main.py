import requests

import pytest
import httpx

from app.core import config

# https://fastapi.tiangolo.com/tutorial/testing/
@pytest.mark.asyncio
async def test_read_api_status(
    client: httpx.AsyncClient,
    settings: config.Settings,
):
    r = await client.get(f'{settings.ROOT_STR}/status')
    assert r.status_code == 200
    assert r.json() == {'status': 'OK'}
    

def test_read_api_status_without_fastapi_with_localhost_port():
    r = requests.get('http://127.0.0.1:3000/status')
    assert r.status_code == 200
    assert r.json() == {
        'status': 'OK'
    }
 