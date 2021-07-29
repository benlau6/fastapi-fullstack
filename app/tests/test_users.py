  
import pytest

from app import schemas
from app.tests.utils.utils import random_email, random_lower_string


@pytest.fixture
def new_user_with_principals_data() -> schemas.UserCreate:
    email = random_email()
    return schemas.UserCreate(
        email=email,
        password=random_lower_string(),
        principals=['user:'+email, 'role:test']
    )


@pytest.fixture
async def new_user_with_principals(new_user_with_principals_data, mock_fastapi_users_instance):
    return await mock_fastapi_users_instance.create_user(new_user_with_principals_data)

    
@pytest.mark.asyncio
async def test_user_has_principals(new_user_with_principals):
    user = new_user_with_principals
    assert user is not None
    assert user.principals == ['user:'+user.email, 'role:test']


@pytest.mark.asyncio
async def test_user_exists(mock_fastapi_users_instance, user):
    user = await mock_fastapi_users_instance.get_user(user.email)
    assert user is not None


@pytest.mark.asyncio
async def test_superuser_exists(mock_fastapi_users_instance, superuser):
    user = await mock_fastapi_users_instance.get_user(superuser.email)
    assert user is not None
    assert user.is_superuser == True

