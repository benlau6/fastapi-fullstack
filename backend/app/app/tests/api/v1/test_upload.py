from typing import Dict
import io

import pytest
import httpx

from app import schemas
from app.core import config
from app.tests.utils.user import get_custom_user_token_headers

# https://fastapi.tiangolo.com/tutorial/testing/

@pytest.fixture()
async def upload_user_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    ) -> Dict[str, str]:
    return await get_custom_user_token_headers(client, settings, principals=['upload:project1:dataset1'])


@pytest.mark.asyncio
async def test_get_upload_info_no_permission(
    client: httpx.AsyncClient, 
    settings: config.Settings,
) -> None:
    r = await client.get(f"{settings.UPLOAD_URL}/info")
    assert 400 <= r.status_code <= 500


@pytest.mark.asyncio
async def test_get_upload_info_super(
    client: httpx.AsyncClient, 
    settings: config.Settings,
    superuser_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.UPLOAD_URL}/info", headers=superuser_token_headers)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_upload_info_has_permission(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    upload_user_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.UPLOAD_URL}/info", headers=upload_user_token_headers)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_upload_file_no_permission(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    upload_user_token_headers: Dict[str, str]
) -> None:
    upload_form_data = {
        'project': 'project_no_permission',
        'dataset': 'dataset1',
        'year': 2020,
        'month': 3,
        'day': 7
    }
    filename = 'test1.jpg'
    upload_files = ('files', (filename, io.BytesIO(b'my file contents'), 'image/jpeg')),

    r = await client.post(f"{settings.UPLOAD_URL}/files", data=upload_form_data, files=upload_files, headers=upload_user_token_headers)
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_post_upload_file(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    upload_user_token_headers: Dict[str, str]
) -> None:
    upload_form_data = {
        'project': 'project1',
        'dataset': 'dataset1',
        'year': 2020,
        'month': 3,
        'day': 7
    }
    filename = 'test1.jpg'
    upload_files = ('files', (filename, io.BytesIO(b'my file contents'), 'image/jpeg')),

    r = await client.post(f"{settings.UPLOAD_URL}/files", data=upload_form_data, files=upload_files, headers=upload_user_token_headers)
    assert r.status_code == 200
    records = r.json()['records']
    assert len(records) == 1
    assert records[0]['owner'] is not None
    assert records[0]['filename'] == filename


@pytest.mark.asyncio
async def test_post_upload_files(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    upload_user_token_headers: Dict[str, str]
) -> None:
    upload_form_data = {
        'project': 'project1',
        'dataset': 'dataset1',
        'year': 2020,
        'month': 3,
        'day': 8
    }
    filename1 = 'test1.jpg'
    filename2 = 'test2.jpg'
    upload_files = [
        ('files', (filename1, io.BytesIO(b'It is a jpg to be uploaded!'), 'image/jpeg')),
        ('files', (filename2, io.BytesIO(b'It is a jpg to be uploaded!'), 'image/jpeg')),
    ]
    
    r = await client.post(f"{settings.UPLOAD_URL}/files", data=upload_form_data, files=upload_files, headers=upload_user_token_headers)
    assert r.status_code == 200
    records = r.json()['records']
    assert len(records) == 2
    assert records[0]['owner'] is not None
    assert records[0]['filename'] == filename1
    assert records[1]['filename'] == filename2
    