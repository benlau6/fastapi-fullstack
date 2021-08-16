import requests

import pytest
from fastapi.testclient import TestClient

from app.core import config

# https://fastapi.tiangolo.com/tutorial/testing/


def test_read_api_status(
    client: TestClient,
    settings: config.Settings,
) -> None:
    r = client.get(f"{settings.ROOT_STR}/status")
    assert r.status_code == 200
    assert r.json() == {"status": "OK"}


def test_read_api_status_without_fastapi_with_localhost_port() -> None:
    r = requests.get("http://127.0.0.1:3000/status")
    assert r.status_code == 200
    assert r.json() == {"status": "OK"}
