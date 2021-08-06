from typing import Dict
import os

import pytest
import httpx

from app import schemas
from app.core import config
from app.tests.utils.user import get_custom_user_token_headers

# https://fastapi.tiangolo.com/tutorial/testing/

@pytest.fixture()
async def download_user_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    ) -> Dict[str, str]:
    return await get_custom_user_token_headers(client, settings, principals=['download:project1:dataset1'])


@pytest.mark.asyncio
async def test_get_download_info_no_permission(
    client: httpx.AsyncClient, 
    settings: config.Settings,
) -> None:
    r = await client.get(f"{settings.DOWNLOAD_URL}/info")
    assert 400 <= r.status_code <= 500


@pytest.mark.asyncio
async def test_get_download_info_super(
    client: httpx.AsyncClient, 
    settings: config.Settings,
    superuser_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.DOWNLOAD_URL}/info", headers=superuser_token_headers)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_download_info_has_permission(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    download_user_token_headers: Dict[str, str]
) -> None:
    r = await client.get(f"{settings.DOWNLOAD_URL}/info", headers=download_user_token_headers)
    assert r.status_code == 200


@pytest.mark.asyncio
async def test_get_download_file_no_permission(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    download_user_token_headers: Dict[str, str]
) -> None:
    download_form_data = {
        'project': 'project_no_permission',
        'dataset': 'dataset1',
        'year': 2020,
        'month': 1,
        'day': 1
    }
    filename = 'test_1.jpg'
    query = schemas.DownloadQuery(**download_form_data)
    
    file_dir = f'{settings.FILE_ROOT_PATH}/{query.base_dir}'
    file_path = f'{file_dir}/{filename}'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, 'wb') as file:
        file.write(b'It is a jpg to be downloaded!')

    r = await client.get(f"{settings.DOWNLOAD_URL}/files/{filename}", params=download_form_data, headers=download_user_token_headers)
    assert 400 <= r.status_code <= 500


@pytest.mark.asyncio
async def test_get_download_file(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    download_user_token_headers: Dict[str, str]
) -> None:
    download_form_data = {
        'project': 'project1',
        'dataset': 'dataset1',
        'year': 2020,
        'month': 1,
        'day': 1
    }
    filename = 'test_1.jpg'
    query = schemas.DownloadQuery(**download_form_data)
    
    file_dir = f'{settings.FILE_ROOT_PATH}/{query.base_dir}'
    file_path = f'{file_dir}/{filename}'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, 'wb') as file:
        file.write(b'It is a jpg to be downloaded!')

    r = await client.get(f"{settings.DOWNLOAD_URL}/files/{filename}", params=download_form_data, headers=download_user_token_headers)
    assert r.status_code == 200
    assert r.content == b'It is a jpg to be downloaded!'


@pytest.mark.asyncio
async def test_get_download_zipped_folder(
    settings: config.Settings,
    client: httpx.AsyncClient, 
    download_user_token_headers: Dict[str, str]
) -> None:
    download_form_data = {
        'project': 'project1',
        'dataset': 'dataset1',
        'year': 2020,
        'month': 1,
        'day': 1
    }
    filename = 'test_1.jpg'
    query = schemas.DownloadQuery(**download_form_data)
    
    file_dir = f'{settings.FILE_ROOT_PATH}/{query.base_dir}'
    file_path = f'{file_dir}/{filename}'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, 'wb') as file:
        file.write(b'It is a jpg to be downloaded!')

    r = await client.get(f"{settings.DOWNLOAD_URL}/files", params=download_form_data, headers=download_user_token_headers)
    assert r.status_code == 200
    assert r.headers['content-type'] == 'application/zip'
