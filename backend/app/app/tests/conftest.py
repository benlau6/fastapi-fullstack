from typing import Generator, List, Optional, Dict
import shutil
import os

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from fastapi_permissions import Allow

from app.main import create_app
from app.core import config
from app import schemas, crud
from app.tests.utils.user import get_normal_user_token_headers, get_superuser_token_headers
from app.tests.utils.utils import random_email, random_lower_string
from app.api import deps
from app.api.deps import Permission
from app.db.mongo import client as mongo_client


test_api_root_str = 'test'
test_file_root_path = '/data/test_files/'
test_mongo_db_name = 'test'
test_config = config.Settings(MONGO_DB_NAME=test_mongo_db_name, ROOT_STR=test_api_root_str, FILE_ROOT_PATH=test_file_root_path)


def get_settings_override():
    return test_config


# it cannot take fixtures
def pytest_sessionstart(session):
    try:
        os.makedirs(test_file_root_path)
    except:
        pass


def pytest_sessionfinish(session, exitstatus):
    try:
        shutil.rmtree(test_file_root_path)
    except:
        pass


@pytest.fixture(scope='session')
def settings() -> config.Settings:
    return test_config


@pytest.fixture(scope='session', autouse=True)
def collection(settings: config.Settings):
    return mongo_client[settings.MONGO_DB_NAME].user


# it auto executes once, then cached returned obj until end of tests, perfect usecase for init user
@pytest.fixture(scope='session', autouse=True)
def normal_user(settings, collection) -> schemas.UserCreate:
    email = settings.FIRST_NORMAL_USER
    password = settings.FIRST_NORMAL_USER_PASSWORD
    user_in = schemas.UserCreate(
        email=email,
        password=password,
        is_verified=True,
    )
    user_id = crud.user.create(collection, document_in=user_in)
    user = crud.user.get(collection, user_id)
    return user


@pytest.fixture(scope='session', autouse=True)
def superuser(settings, collection) -> schemas.UserCreate:
    email = settings.FIRST_SUPERUSER
    password = settings.FIRST_SUPERUSER_PASSWORD
    user_in = schemas.UserCreate(
        email=email,
        password=password,
        is_superuser=True,
        is_verified=True,
    )
    user_id = crud.user.create(collection, document_in=user_in)
    user = crud.user.get(collection, user_id)
    return user


# it will be executed once if called by a function
@pytest.fixture
def new_user(collection) -> schemas.UserCreate:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user_id = crud.user.create(collection, document_in=user_in)
    user = crud.user.get(collection, user_id)
    return user


@pytest.fixture
def superuser_token_headers(
    client: TestClient, 
    settings: config.Settings, 
    superuser
    ) -> Dict[str, str]:
    return get_superuser_token_headers(client, settings, superuser)


@pytest.fixture
def normal_user_token_headers(
    client: TestClient, 
    settings: config.Settings, 
    normal_user
    ) -> Dict[str, str]:
    return get_normal_user_token_headers(client, settings, normal_user)


@pytest.fixture
def app(settings) -> FastAPI:
    main_app = create_app(settings)
    main_app.dependency_overrides[deps.get_settings] = get_settings_override

    @main_app.get("/test-current-user")
    def _(user: schemas.UserFromDB = Depends(deps.get_current_user)):
        return user

    @main_app.get("/test-current-active-user")
    def _(user: schemas.UserFromDB = Depends(deps.get_current_active_user)):
        return user

    @main_app.get("/test-current-active-superuser")
    def _(user: schemas.UserFromDB = Depends(deps.get_current_active_superuser)):
        return user

    example_acl = [(Allow, "role:admin", "view")]
    @main_app.get("/test-user-permission")
    def _(acls: list = Permission('view', example_acl)):
        return {'status': 'OK'}

    yield main_app


@pytest.fixture
def client(app) -> Generator:
    with TestClient(app) as c:
        yield c