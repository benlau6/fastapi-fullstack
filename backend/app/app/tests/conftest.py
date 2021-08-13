from typing import Generator, List, Optional, Dict, Any
import shutil
import os

import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from fastapi_permissions import Allow

from app.main import create_app
from app.core import config
from app import schemas, crud
from app.tests.utils.user import (
    get_normal_user_token_headers,
    get_superuser_token_headers,
)
from app.tests.utils.utils import random_email, random_lower_string
from app.api import deps
from app.api.deps import Permission
from app.db.mongo import client as mongo_client


test_file_root_path = "/data/test_files/"
test_mongo_db_name = "test"
# ROOT_STR = '' because inside the container, there is no proxy,
# then the original routes are mounted with no root str
test_config = config.Settings(
    MONGO_DB_NAME=test_mongo_db_name, ROOT_STR="", FILE_ROOT_PATH=test_file_root_path
)


def get_settings_override() -> config.Settings:
    return test_config


# it cannot take fixtures
def pytest_sessionstart(session: Any) -> None:
    try:
        os.makedirs(test_file_root_path)
    except Exception:
        pass


def pytest_sessionfinish(session: Any, exitstatus: Any) -> None:
    try:
        shutil.rmtree(test_file_root_path)
    except Exception:
        pass


@pytest.fixture(scope="session")
def settings() -> config.Settings:
    return test_config


@pytest.fixture
def superuser_token_headers(
    client: TestClient, settings: config.Settings
) -> Dict[str, str]:
    return get_superuser_token_headers(client, settings)


@pytest.fixture
def normal_user_token_headers(
    client: TestClient, settings: config.Settings
) -> Dict[str, str]:
    return get_normal_user_token_headers(client, settings)


# autouse allows it to drop after all tests, but not right after some tests needing that.
@pytest.fixture(scope="session", autouse=True)
def collection(settings: config.Settings) -> Any:
    collection = mongo_client[settings.MONGO_DB_NAME].user
    # init db with super user
    superuser = crud.user.get_by_email(collection, email=settings.FIRST_SUPERUSER)
    if not superuser:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(collection, document_in=user_in)

    user = crud.user.get_by_email(collection, email=settings.FIRST_NORMAL_USER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_NORMAL_USER,
            password=settings.FIRST_NORMAL_USER_PASSWORD,
            is_verified=True,
        )
        crud.user.create(collection, document_in=user_in)
    yield collection
    # drop test db after all tests
    mongo_client.drop_database("test")


@pytest.fixture
def app(settings: config.Settings) -> Generator:
    main_app = create_app(settings)
    main_app.dependency_overrides[deps.get_settings] = get_settings_override

    @main_app.get("/test-current-user", response_model=schemas.UserFromDB)
    def dummy1(
        user: schemas.UserFromDB = Depends(deps.get_current_user),
    ) -> schemas.UserFromDB:
        return user

    @main_app.get("/test-current-active-user", response_model=schemas.UserFromDB)
    def dummy2(
        user: schemas.UserFromDB = Depends(deps.get_current_active_user),
    ) -> schemas.UserFromDB:
        return user

    @main_app.get("/test-current-active-superuser", response_model=schemas.UserFromDB)
    def dummy3(
        user: schemas.UserFromDB = Depends(deps.get_current_active_superuser),
    ) -> schemas.UserFromDB:
        return user

    example_acl = [(Allow, "role:admin", "view")]

    @main_app.get("/test-user-permission")
    def dummy4(acls: list = Permission("view", example_acl)) -> Dict[str, str]:
        return {"status": "OK"}

    yield main_app


@pytest.fixture
def client(app: Any) -> Generator:
    with TestClient(app) as c:
        yield c
