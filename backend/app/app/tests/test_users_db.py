  
import pytest

from app.api.fastapi_users_utils import fastapi_users_instance


@pytest.mark.asyncio
async def test_created_user_exists(new_user):
    found_user = await fastapi_users_instance.get_user(new_user.email)
    assert found_user is not None
    assert found_user.email == new_user.email
    assert found_user.principals == new_user.principals


@pytest.mark.asyncio
async def test_users_exists(client, settings, superuser_token_headers):
    r = await client.get(f'{settings.USERS_URL}', headers=superuser_token_headers)
    all_users = r.json()
    assert len(all_users) >= 2