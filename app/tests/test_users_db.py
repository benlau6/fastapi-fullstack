  
import pytest

from app import schemas
from app.api.fastapi_users_utils import fastapi_users_instance


@pytest.mark.asyncio
async def test_created_user_exists(new_user):
    created_user = await fastapi_users_instance.create_user(new_user)
    found_user = await fastapi_users_instance.get_user(new_user.email)
    assert found_user is not None
    assert found_user.email == new_user.email
    assert found_user.principals == created_user.principals


@pytest.mark.asyncio
async def test_users_exists(client, settings):
    r = await client.get(f'{settings.USERS_URL}/all')
    all_users = r.json()
    assert len(all_users) >= 2