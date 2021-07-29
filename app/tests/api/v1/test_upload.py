#from typing import Dict
#import io
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
#async def upload_user_token_headers(
#    client: TestClient, 
#    settings: config.Settings, 
#    db
#    ) -> Dict[str, str]:
#    return await authentication_token_from_email(
#        client=client, 
#        settings=settings, 
#        db=db,
#        email=settings.EMAIL_TEST_USER, 
#    )
#
#
##@pytest.mark.asyncio
##async def test_get_upload_info_not_in_scopes(
##    client: TestClient, 
##    settings: config.Settings,
##    normal_user_token_headers: Dict[str, str]
##) -> None:
##    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/upload/info", headers=normal_user_token_headers)
##    assert r.status_code == 401
#
#
#@pytest.mark.asyncio
#async def test_get_upload_info_super(
#    client: TestClient, 
#    settings: config.Settings,
#    superuser_token_headers: Dict[str, str]
#) -> None:
#    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/upload/info", headers=superuser_token_headers)
#    assert r.status_code == 200
#
#
#@pytest.mark.asyncio
#async def test_get_upload_info_in_scopes(
#    settings: config.Settings,
#    client: TestClient, 
#    upload_user_token_headers: Dict[str, str]
#) -> None:
#    r = await client.get(f"{settings.ROOT_STR}{settings.API_V1_STR}/upload/info", headers=upload_user_token_headers)
#    assert r.status_code == 200
#
#
#@pytest.mark.asyncio
#async def test_post_upload_file(
#    settings: config.Settings,
#    client: TestClient, 
#    upload_user_token_headers: Dict[str, str]
#) -> None:
#    upload_form_data = {
#        'project': 'project1',
#        'dataset': 'dataset1',
#        'year': 2020,
#        'month': 3,
#        'day': 7
#    }
#    filename = 'test1.jpg'
#    upload_files = ('files', (filename, io.BytesIO(b'my file contents'), 'image/jpeg')),
#
#    form = schemas.UploadForm(**upload_form_data)
#    r = await client.post(f"{settings.ROOT_STR}{settings.API_V1_STR}/upload/files", data=upload_form_data, files=upload_files, headers=upload_user_token_headers)
#    records = r.json()['records']
#    assert r.status_code == 200
#    assert len(records) == 1
#    assert records[0]['owner'] == settings.EMAIL_TEST_USER
#    assert records[0]['filename'] == filename
#
#
#@pytest.mark.asyncio
#async def test_post_upload_files(
#    settings: config.Settings,
#    client: TestClient, 
#    upload_user_token_headers: Dict[str, str]
#) -> None:
#    upload_form_data = {
#        'project': 'project1',
#        'dataset': 'dataset1',
#        'year': 2020,
#        'month': 3,
#        'day': 8
#    }
#    form = schemas.UploadForm(**upload_form_data)
#    filename1 = 'test1.jpg'
#    filename2 = 'test2.jpg'
#    upload_files = [
#        ('files', (filename1, io.BytesIO(b'It is a jpg to be uploaded!'), 'image/jpeg')),
#        ('files', (filename2, io.BytesIO(b'It is a jpg to be uploaded!'), 'image/jpeg')),
#    ]
#    
#    r = await client.post(f"{settings.ROOT_STR}{settings.API_V1_STR}/upload/files", data=upload_form_data, files=upload_files, headers=upload_user_token_headers)
#    records = r.json()['records']
#    assert r.status_code == 200
#    assert len(records) == 2
#    assert records[0]['owner'] == settings.EMAIL_TEST_USER
#    assert records[0]['filename'] == filename1
#    assert records[1]['filename'] == filename2
    