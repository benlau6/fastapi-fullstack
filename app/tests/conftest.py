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

from app.api.fastapi_users_utils import fastapi_users_instance
from app.main import create_app
from app.api import deps
from app.core import config
from app import schemas
from app.tests.utils.user import get_normal_user_token_headers, get_superuser_token_headers
from app.tests.utils.utils import random_email, random_lower_string


test_root_path = '/data/fastapi'

# DATABASE_URL DOES NOT CHANGE
modified_settings = config.Settings(DATABASE_URL='sqlite:///data/fastapi/test.db', ROOT_STR='', FILE_ROOT_PATH=test_root_path)
main_app = create_app()
#
#
def get_settings_override():
    return modified_settings.DATABASE_URL

@pytest.fixture(scope='session')
def settings():
    return modified_settings
#

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


@pytest.fixture
async def new_user() -> schemas.UserCreate:
    email=random_email()
    obj_in = schemas.UserCreate(
        email=email,
        password=random_lower_string(),
        principals=['user:'+email, 'role:test']
    )
    return obj_in


@pytest.fixture
def new_inactive_user_data() -> schemas.UserCreate:
    return schemas.UserCreate(
        email=random_email(),
        password=random_lower_string(),
        is_active=False,
    )


@pytest.fixture
def new_verified_user_data() -> schemas.UserCreate:
    return schemas.UserCreate(
        email=random_email(),
        password=random_lower_string(),
        is_verified=True,
    )


@pytest.fixture
def new_superuser_in_data() -> schemas.UserCreate:
    return schemas.UserCreate(
        email=random_email(),
        password=random_lower_string(),
        is_superuser=True,
        is_verified=True,
    )

# it auto executes once, for tortoise orm, making app as created_app() is for this not to be ignored, without specifying db_url, it stored in memory
@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(
        ["app.models"],
        db_url=modified_settings.DATABASE_URL
    )
    request.addfinalizer(finalizer)

# it auto executes once, then cached returned obj until end of tests, perfect usecase for init user
@pytest.fixture(scope='session', autouse=True)
async def normal_user() -> schemas.UserCreate:
    email = 'user@gmail.com'
    obj_in = schemas.UserCreate(
        email=email,
        password='password',
        is_verified=True,
        principals=['user:'+email]
    )
    await fastapi_users_instance.create_user(obj_in)
    return obj_in


@pytest.fixture(scope='session', autouse=True)
async def superuser() -> schemas.UserCreate:
    obj_in = schemas.UserCreate(
        email='admin@gmail.com',
        password='password',
        is_superuser=True,
        is_verified=True,
        principals=['role:admin']
    )
    await fastapi_users_instance.create_user(obj_in)
    return obj_in


@pytest.fixture
async def app(settings, normal_user, superuser):
    main_app.dependency_overrides[deps.get_settings] = get_settings_override  
    main_app.DATABASE_URL = modified_settings.DATABASE_URL

    @main_app.get("/test-current-user")
    def test_current_user(user: schemas.UserInDB = Depends(fastapi_users_instance.current_user())):
        return user

    @main_app.get("/test-current-active-user")
    def test_current_active_user(
        user: schemas.UserInDB = Depends(fastapi_users_instance.current_user(active=True)),
    ):
        return user

    @main_app.get("/test-current-superuser")
    def test_current_superuser(
        user: schemas.UserInDB = Depends(
            fastapi_users_instance.current_user(active=True, superuser=True)
        ),
    ):
        return user

    #@app.on_event("startup")
    #async def init_orm() -> None:  # pylint: disable=W0612


    async with LifespanManager(main_app):
        yield main_app


@pytest.fixture
async def client(app) -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(app=app, base_url="http://meaningless_but_mandatory_url") as client:
        yield client

#from tortoise import Tortoise
#
#
#def pytest_sessionstart(session):
#    async def init():
#        # Here we create a SQLite DB using file "db.sqlite3"
#        #  also specify the app name of "models"
#        #  which contain models from "app.models"
#        await Tortoise.init(
#            db_url='sqlite://db.sqlite3',
#            modules={'models': ['app.models']}
#        )
#        # Generate the schema
#        await Tortoise.generate_schemas()

#
def pytest_sessionfinish(session, exitstatus):
    try:
        shutil.rmtree(test_root_path)
    except:
        pass


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