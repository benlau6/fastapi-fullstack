import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.parametrize(
    "path,method",
    [
        ("/v1/users", "GET"),
        ("/v1/auth/login/access-token", "POST"),
        ("/v1/auth/logout", "POST"),
        ("/v1/upload/info", "GET"),
        ("/v1/upload/files", "POST"),
        ("/v1/download/info", "GET"),
        ("/v1/download/files", "GET"),
        ("/v1/download/files/dummy_file", "GET"),
        ("/test-current-user", "GET"),
        ("/test-current-active-user", "GET"),
        ("/test-current-active-superuser", "GET"),
    ],
)
def test_route_exists(client: TestClient, path: str, method: str) -> None:
    response = client.request(method, path)
    assert response.status_code not in (
        status.HTTP_404_NOT_FOUND,
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )
