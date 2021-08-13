from typing import Any, Dict, Union
import os

import pytest
from fastapi.testclient import TestClient

from app import schemas
from app.core import config
from app.tests.utils.user import get_custom_user_token_headers

# https://fastapi.tiangolo.com/tutorial/testing/


@pytest.fixture
def download_user_token_headers(
    client: TestClient, settings: config.Settings, collection: Any
) -> Dict[str, str]:
    return get_custom_user_token_headers(
        client,
        settings,
        collection,
        scopes=["download:project1:dataset1"] + settings.SCOPES_DOWNLOAD,
    )


def test_get_download_info_no_permission(
    client: TestClient,
    settings: config.Settings,
) -> None:
    r = client.get(f"{settings.DOWNLOAD_URL}/info")
    assert 400 <= r.status_code <= 500


def test_get_download_info_super(
    client: TestClient,
    settings: config.Settings,
    superuser_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.DOWNLOAD_URL}/info", headers=superuser_token_headers)
    assert r.status_code == 200


def test_get_download_info_has_permission(
    settings: config.Settings,
    client: TestClient,
    download_user_token_headers: Dict[str, str],
) -> None:
    r = client.get(f"{settings.DOWNLOAD_URL}/info", headers=download_user_token_headers)
    print(download_user_token_headers)
    assert r.status_code == 200


def test_get_download_file_no_permission(
    settings: config.Settings,
    client: TestClient,
    download_user_token_headers: Dict[str, str],
) -> None:
    # https://github.com/python/mypy/issues/3176
    download_form_data: Dict[str, Union[int, str]]  = {
        "project": "project_no_permission",
        "dataset": "dataset1",
        "year": 2020,
        "month": 1,
        "day": 1,
    }
    filename = "test_1.jpg"
    query = schemas.DownloadQuery(**download_form_data)

    file_dir = f"{settings.FILE_ROOT_PATH}/{query.base_dir}"
    file_path = f"{file_dir}/{filename}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, "wb") as file:
        file.write(b"It is a jpg to be downloaded!")

    r = client.get(
        f"{settings.DOWNLOAD_URL}/files/{filename}",
        params=download_form_data,
        headers=download_user_token_headers,
    )
    assert 400 <= r.status_code <= 500


def test_get_download_file(
    settings: config.Settings,
    client: TestClient,
    download_user_token_headers: Dict[str, str],
) -> None:
    download_form_data: Dict[str, Union[int, str]] = {
        "project": "project1",
        "dataset": "dataset1",
        "year": 2020,
        "month": 1,
        "day": 1,
    }
    filename = "test_1.jpg"
    query = schemas.DownloadQuery(**download_form_data)

    file_dir = f"{settings.FILE_ROOT_PATH}/{query.base_dir}"
    file_path = f"{file_dir}/{filename}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, "wb") as file:
        file.write(b"It is a jpg to be downloaded!")

    r = client.get(
        f"{settings.DOWNLOAD_URL}/files/{filename}",
        params=download_form_data,
        headers=download_user_token_headers,
    )
    assert r.status_code == 200
    assert r.content == b"It is a jpg to be downloaded!"


def test_get_download_zipped_folder(
    settings: config.Settings,
    client: TestClient,
    download_user_token_headers: Dict[str, str],
) -> None:
    download_form_data: Dict[str, Union[int, str]] = {
        "project": "project1",
        "dataset": "dataset1",
        "year": 2020,
        "month": 1,
        "day": 1,
    }
    filename = "test_1.jpg"
    query = schemas.DownloadQuery(**download_form_data)

    file_dir = f"{settings.FILE_ROOT_PATH}/{query.base_dir}"
    file_path = f"{file_dir}/{filename}"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, "wb") as file:
        file.write(b"It is a jpg to be downloaded!")

    r = client.get(
        f"{settings.DOWNLOAD_URL}/files",
        params=download_form_data,
        headers=download_user_token_headers,
    )
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/zip"
