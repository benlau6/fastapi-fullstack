#from typing import Dict
#import os
#
#import pytest
#from async_asgi_testclient import TestClient
#
#from app import schemas
#from app.core import config
#from app.tests.utils.user import authentication_token_from_email
#
## https://fastapi.tiangolo.com/tutorial/testing/
#
#@pytest.fixture(scope="module")
#@pytest.mark.asyncio
#async def download_user_token_headers(
#    client: TestClient, 
#    settings: config.Settings, 
#    db
#    ) -> Dict[str, str]:
#    return await authentication_token_from_email(
#        client=client, 
#        settings=settings, 
#        email=settings.EMAIL_TEST_USER, 
#        db=db
#    )
#
#
##@pytest.mark.asyncio
##async def test_get_download_info_not_in_scopes(
##    client: TestClient, 
##    settings: config.Settings,
##    normal_user_token_headers: Dict[str, str]
##) -> None:
##    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/download/info", headers=normal_user_token_headers)
##    assert r.status_code == 401
#
#
#@pytest.mark.asyncio
#async def test_get_download_info_super(
#    client: TestClient, 
#    settings: config.Settings,
#    superuser_token_headers: Dict[str, str]
#) -> None:
#    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/download/info", headers=superuser_token_headers)
#    assert r.status_code == 200
#
#
#@pytest.mark.asyncio
#async def test_get_download_info_in_scopes(
#    settings: config.Settings,
#    client: TestClient, 
#    download_user_token_headers: Dict[str, str]
#) -> None:
#    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/download/info", headers=download_user_token_headers)
#    assert r.status_code == 200
#
#
#@pytest.mark.asyncio
#async def test_get_download_file(
#    settings: config.Settings,
#    client: TestClient, 
#    download_user_token_headers: Dict[str, str]
#) -> None:
#    download_form_data = {
#        'project': 'project1',
#        'dataset': 'dataset1',
#        'year': 2020,
#        'month': 1,
#        'day': 1
#    }
#    filename = 'test_1.jpg'
#    form = schemas.DownloadForm(**download_form_data)
#    
#    file_dir = f'{settings.FILE_ROOT_PATH}/{form.base_dir}'
#    file_path = f'{file_dir}/{filename}'
#    if not os.path.exists(file_dir):
#        os.makedirs(file_dir)
#    with open(file_path, 'wb') as file:
#        file.write(b'It is a jpg to be downloaded!')
#
#    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/download/files/{filename}", data=download_form_data, headers=download_user_token_headers)
#    assert r.status_code == 200
#    assert r.content == b'It is a jpg to be downloaded!'
#
#
#@pytest.mark.asyncio
#async def test_get_download_zipped_folder(
#    settings: config.Settings,
#    client: TestClient, 
#    download_user_token_headers: Dict[str, str]
#) -> None:
#    download_form_data = {
#        'project': 'project1',
#        'dataset': 'dataset1',
#        'year': 2020,
#        'month': 1,
#        'day': 1
#    }
#    filename = 'test_1.jpg'
#    form = schemas.DownloadForm(**download_form_data)
#    
#    file_dir = f'{settings.FILE_ROOT_PATH}/{form.base_dir}'
#    file_path = f'{file_dir}/{filename}'
#    if not os.path.exists(file_dir):
#        os.makedirs(file_dir)
#    with open(file_path, 'wb') as file:
#        file.write(b'It is a jpg to be downloaded!')
#
#    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/download/files", data=download_form_data, headers=download_user_token_headers)
#    assert r.status_code == 200
#    assert r.headers['content-type'] == 'application/zip'
