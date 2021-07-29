import pytest
import httpx

from app.core import config

@pytest.mark.asyncio
async def test_superuser_token_headers(
    superuser_token_headers
):
    assert superuser_token_headers == 1