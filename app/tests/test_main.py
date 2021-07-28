import requests
from async_asgi_testclient import TestClient

import pytest

from app.core import config

# https://fastapi.tiangolo.com/tutorial/testing/
@pytest.mark.asyncio
async def test_read_api_status(
    client: TestClient,
    settings: config.Settings,
):
    r = await client.get(f'{settings.ROOT_STR}/status')
    assert r.status_code == 200
    assert r.json() == {'status': 'OK'}

#curl -H 'Host: api.docker.localhost' http://host.docker.internal/api/status
def test_read_api_status_without_fastapi(headers):
    r = requests.get('http://host.docker.internal/api/status', headers=headers)
    assert r.status_code == 200
    assert r.json() == {
        'status': 'OK'
    }
    

def test_read_api_status_without_fastapi_with_localhost_port(client: TestClient):
    r = requests.get('http://127.0.0.1:3000/status')
    assert r.status_code == 200
    assert r.json() == {
        'status': 'OK'
    }
 
