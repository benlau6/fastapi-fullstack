import random
import string
from typing import Dict

import pytest

from fastapi.testclient import TestClient

from app.core import config


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"

@pytest.mark.asyncio
async def get_superuser_token_headers(client: TestClient, settings: config.Settings) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post(f"{settings.ROOT_STR}{settings.API_V1_STR}/auth/jwt/login", form=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
