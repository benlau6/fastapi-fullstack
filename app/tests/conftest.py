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
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import get_password_hash
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication, CookieAuthentication

from app.schemas import UserInDB, User, UserCreate, UserUpdate

from app.main import app as main_app
from app.api import deps
from app.core import config
from app import schemas
from app.tests.utils.user import get_normal_user_token_headers, get_superuser_token_headers


test_root_path = '/data/fastapi'
modified_settings = config.Settings(DATABASE_URL='sqlite:///data/fastapi/test.db', ROOT_STR='', FILE_ROOT_PATH=test_root_path)
#
#
def get_settings_override():
    return modified_settings

@pytest.fixture
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


guinevere_password_hash = get_password_hash("password")
angharad_password_hash = get_password_hash("password")
viviane_password_hash = get_password_hash("password")
lancelot_password_hash = get_password_hash("password")
excalibur_password_hash = get_password_hash("password")


@pytest.fixture
def user() -> schemas.UserInDB:
    return schemas.UserInDB(
        email="king.arthur@camelot.bt",
        hashed_password=guinevere_password_hash,
    )


@pytest.fixture
def inactive_user() -> schemas.UserInDB:
    return schemas.UserInDB(
        email="percival@camelot.bt",
        hashed_password=angharad_password_hash,
        is_active=False,
    )


@pytest.fixture
def verified_user() -> schemas.UserInDB:
    return schemas.UserInDB(
        email="lake.lady@camelot.bt",
        hashed_password=excalibur_password_hash,
        is_verified=True,
    )


@pytest.fixture
def superuser() -> schemas.UserInDB:
    return schemas.UserInDB(
        email="merlin@camelot.bt",
        hashed_password=viviane_password_hash,
        is_superuser=True,
    )


@pytest.fixture
def verified_superuser() -> schemas.UserInDB:
    return schemas.UserInDB(
        email="the.real.merlin@camelot.bt",
        hashed_password=viviane_password_hash,
        is_superuser=True,
        is_verified=True,
    )


@pytest.fixture
def mock_user_db(
    user, verified_user, inactive_user, superuser, verified_superuser
) -> BaseUserDatabase:
    class MockUserDatabase(BaseUserDatabase[schemas.UserInDB]):
        async def get(self, id: UUID4) -> Optional[schemas.UserInDB]:
            if id == user.id:
                return user
            if id == verified_user.id:
                return verified_user
            if id == inactive_user.id:
                return inactive_user
            if id == superuser.id:
                return superuser
            if id == verified_superuser.id:
                return verified_superuser
            return None

        async def get_by_email(self, email: str) -> Optional[schemas.UserInDB]:
            lower_email = email.lower()
            if lower_email == user.email.lower():
                return user
            if lower_email == verified_user.email.lower():
                return verified_user
            if lower_email == inactive_user.email.lower():
                return inactive_user
            if lower_email == superuser.email.lower():
                return superuser
            if lower_email == verified_superuser.email.lower():
                return verified_superuser
            return None

        async def create(self, user: schemas.UserInDB) -> schemas.UserInDB:
            return user

        async def update(self, db_user: schemas.UserInDB, user: schemas.UserInDB) -> schemas.UserInDB:
            return user

        async def delete(self, user: schemas.UserInDB) -> None:
            pass

    return MockUserDatabase(schemas.UserInDB)


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(
        ["app.models"],
        db_url=modified_settings.DATABASE_URL,
    )
    request.addfinalizer(finalizer)


@pytest.fixture
def mock_fastapi_users_instance(settings, mock_user_db):
    jwt_authentication = JWTAuthentication(
        secret=settings.SECRET_KEY, 
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES//60, 
        tokenUrl=settings.TOKEN_URL
    )

    cookie_authentication = CookieAuthentication(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES//60,
    )

    mock_fastapi_users_instance = FastAPIUsers(
        db=mock_user_db,
        auth_backends=[jwt_authentication, cookie_authentication],
        user_model=User,
        user_create_model=UserCreate,
        user_update_model=UserUpdate,
        user_db_model=UserInDB,
    )
    return mock_fastapi_users_instance


@pytest.fixture
async def app(settings, mock_fastapi_users_instance):
    main_app.dependency_overrides[deps.get_settings] = get_settings_override  
    main_app.DATABASE_URL = 'sqlite:///data/fastapi/test/test.db'

    @main_app.get("/test-current-user")
    def test_current_user(user: schemas.UserInDB = Depends(mock_fastapi_users_instance.current_user())):
        return user

    @main_app.get("/test-current-active-user")
    def test_current_active_user(
        user: schemas.UserInDB = Depends(mock_fastapi_users_instance.current_user(active=True)),
    ):
        return user

    @main_app.get("/test-current-superuser")
    def test_current_superuser(
        user: schemas.UserInDB = Depends(
            mock_fastapi_users_instance.current_user(active=True, superuser=True)
        ),
    ):
        return user

    async with LifespanManager(main_app):
        yield main_app


@pytest.fixture
async def client(app) -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(app=app, base_url="http://meaningless_but_mandatory_url") as client:
        yield client


#
##def pytest_sessionfinish(session, exitstatus):
#    
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
    user
    ) -> Dict[str, str]:
    return await get_normal_user_token_headers(client, settings, user)