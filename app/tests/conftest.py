from typing import Dict, Generator
import shutil

import pytest
import asyncio
from async_asgi_testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.main import app
from app.core import config
from app.api import deps
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


test_root_path = '/data/fastapi'
modified_settings = config.Settings(DATABASE_URL='sqlite:///data/fastapi/test.db', ROOT_STR='', FILE_ROOT_PATH=test_root_path)


def get_settings_override():
    return modified_settings

app.dependency_overrides[deps.get_settings] = get_settings_override  
app.DATABASE_URL = 'sqlite:///data/fastapi/test/test.db'


#def pytest_sessionfinish(session, exitstatus):
    

def pytest_sessionfinish(session, exitstatus):
    try:
        shutil.rmtree(test_root_path)
    except:
        pass
    

@pytest.fixture(scope="session")
def headers() -> Dict[str, str]:
    headers = {
        'Host': 'api.docker.localhost'
    }
    return headers


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture(scope="session")
def db():
    return None


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(
        ["app.models"],
        db_url=modified_settings.DATABASE_URL,
    )
    request.addfinalizer(finalizer)


@pytest.fixture(scope="module")
async def client() -> Generator:
    async with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def settings():
    return modified_settings


@pytest.fixture(scope="module")
async def superuser_token_headers(client: TestClient, settings: config.Settings) -> Dict[str, str]:
    return await get_superuser_token_headers(client, settings)


@pytest.fixture(scope="module")
async def normal_user_token_headers(
    client: TestClient, 
    settings: config.Settings, 
    db,
    ) -> Dict[str, str]:
    return await authentication_token_from_email(
        client=client, settings=settings, db=db, email=settings.EMAIL_TEST_USER, 
    )