import pytest
import httpx
from fastapi import status

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path,method",
    [
        ("/v1/auth/register", "POST"),
        ("/v1/auth/request-verify-token", "POST"),
        ("/v1/auth/verify", "POST"),
        ("/v1/auth/forgot-password", "POST"),
        ("/v1/auth/reset-password", "POST"),
        ("/v1/auth/jwt/login", "POST"),
        ("/v1/auth/cookie/login", "POST"),
        ("/v1/auth/cookie/logout", "POST"),
        ("/v1/users", "GET"),
        ("/v1/users/d35d213e-f3d8-4f08-954a-7e0d1bea286f", "GET"), # dummy uuid4 to test it exists
        ("/v1/users/d35d213e-f3d8-4f08-954a-7e0d1bea286f", "PATCH"),
        ("/v1/users/d35d213e-f3d8-4f08-954a-7e0d1bea286f", "DELETE"),
        ("/v1/upload/info", "GET"),
        ("/v1/upload/files", "POST"),
        ("/v1/download/info", "GET"),
        ("/v1/download/files", "GET"),
        ("/v1/download/files/d35d213e-f3d8-4f08-954a-7e0d1bea286f", "GET"),
    ],
)
async def test_route_exists(client: httpx.AsyncClient, path: str, method: str):
    response = await client.request(method, path)
    assert response.status_code not in (
        status.HTTP_404_NOT_FOUND,
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )