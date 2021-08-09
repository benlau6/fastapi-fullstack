import asyncio
from typing import AsyncGenerator, List, Optional, Dict
import shutil

import httpx
import pytest
from fastapi import Depends
from pydantic import UUID4
from starlette.applications import ASGIApp
from asgi_lifespan import LifespanManager
from tortoise.contrib.test import finalizer, initializer
from fastapi_permissions import Allow

from app.main import create_app

from app.core import config
from app import schemas
from app.tests.utils.user import get_normal_user_token_headers, get_superuser_token_headers
from app.tests.utils.utils import random_email, random_lower_string
from app.api import deps
from app.api.deps import Permission
from app.api.fastapi_users_utils import fastapi_users_instance

test_api_root_str = ''
test_root_path = '/data/files'
test_database_url = 'sqlite:///data/db/test.db'
test_config = config.Settings(DATABASE_URL=test_database_url, ROOT_STR=test_api_root_str, FILE_ROOT_PATH=test_root_path)


def get_settings_override():
    return test_config


# it cannot take fixtures
def pytest_sessionstart(session):
    pass


def pytest_sessionfinish(session, exitstatus):
    try:
        shutil.rmtree(test_root_path)
    except:
        pass


@pytest.fixture(scope='session')
def settings() -> config.Settings:
    return test_config


@pytest.fixture
def headers() -> Dict[str, str]:
    headers = {
        'Host': 'api.docker.localhost'
    }
    return headers


@pytest.fixture(scope="session")
def event_loop():
    """Force the pytest-asyncio loop to be the main one."""
    loop = asyncio.get_event_loop()
    yield loop


# it auto executes once, for tortoise orm, making app as created_app() is for this not to be ignored, without specifying db_url, it stored in memory
@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request, settings):
    initializer(
        ["app.models"],
        db_url=settings.DATABASE_URL
    )
    request.addfinalizer(finalizer)


# it auto executes once, then cached returned obj until end of tests, perfect usecase for init user
@pytest.fixture(scope='session', autouse=True)
async def normal_user(settings) -> schemas.UserCreate:
    email = settings.FIRST_NORMAL_USER
    obj_in = schemas.UserCreate(
        email=email,
        password='password',
        is_verified=True,
        principals=['user:'+email]
    )
    await fastapi_users_instance.create_user(obj_in)
    return obj_in


@pytest.fixture(scope='session', autouse=True)
async def superuser(settings) -> schemas.UserCreate:
    email = settings.FIRST_SUPERUSER
    obj_in = schemas.UserCreate(
        email=email,
        password='password',
        is_superuser=True,
        is_verified=True,
        principals=['role:admin', 'user:'+email]
    )
    await fastapi_users_instance.create_user(obj_in)
    return obj_in


# it will be executed once if called by a function
@pytest.fixture
async def new_user() -> schemas.UserCreate:
    email=random_email()
    obj_in = schemas.UserCreate(
        email=email,
        password=random_lower_string(),
        principals=['user:'+email]
    )
    new_user = await fastapi_users_instance.create_user(obj_in)
    return new_user


@pytest.fixture
async def superuser_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    superuser
    ) -> Dict[str, str]:
    return await get_superuser_token_headers(client, settings, superuser)


@pytest.fixture
async def normal_user_token_headers(
    client: httpx.AsyncClient, 
    settings: config.Settings, 
    normal_user
    ) -> Dict[str, str]:
    return await get_normal_user_token_headers(client, settings, normal_user)


@pytest.fixture
async def app():
    main_app = create_app()
    main_app.dependency_overrides[deps.get_settings] = get_settings_override  

    @main_app.get("/test-current-user")
    def _(user: schemas.UserInDB = Depends(fastapi_users_instance.current_user())):
        return user

    @main_app.get("/test-current-active-user")
    def _(
        user: schemas.UserInDB = Depends(fastapi_users_instance.current_user(active=True)),
    ):
        return user

    @main_app.get("/test-current-superuser")
    def _(
        user: schemas.UserInDB = Depends(
            fastapi_users_instance.current_user(active=True, superuser=True)
        ),
    ):
        return user

    example_acl = [(Allow, "role:admin", "view")]
    @main_app.get("/test-user-permission")
    def _(
        acls: list = Permission('view', example_acl),
    ):
        return {'status': 'OK'}

    async with LifespanManager(main_app):
        yield main_app


@pytest.fixture
async def client(app) -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(app=app, base_url="http://meaningless_but_mandatory_url") as client:
        yield client