from app import crud, schemas
from app.core.security import verify_password
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(collection) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    user_id = crud.user.create(collection, document_in=user_in)
    assert user_id


def test_get_user(collection, new_user) -> None:
    found_user = crud.user.get(collection, new_user['_id'])
    assert found_user
    assert 'hashed_password' in found_user
    assert 'password' not in found_user


def test_get_user_by_email(collection, new_user) -> None:
    found_user = crud.user.get(collection, new_user['_id'])
    found_user2 = crud.user.get_by_email(collection, found_user['email'])
    assert found_user2
    assert 'hashed_password' in found_user2
    assert 'password' not in found_user2
    assert found_user['email'] == found_user2['email']


def test_update_user(collection, new_user) -> None:
    new_password = random_lower_string()
    user_in_update = schemas.UserUpdate(password=new_password)
    matched_count, modified_count = crud.user.update(collection, id=new_user['_id'], document_in=user_in_update)
    updated_user = crud.user.get(collection, id=new_user['_id'])
    assert verify_password(new_password, updated_user['hashed_password'])
    assert matched_count == 1
    assert modified_count == 1


def test_delete_user(collection, new_user) -> None:
    deleted_count = crud.user.delete(collection, id=new_user['_id'])
    assert deleted_count == 1


def test_authenticate_user(collection) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password)
    crud.user.create(collection, document_in=user_in)
    authenticated_user = crud.user.authenticate(collection, email=email, password=password)
    assert authenticated_user['email'] == email


def test_not_authenticate_user(collection) -> None:
    email = random_email()
    password = random_lower_string()
    authenticated_user = crud.user.authenticate(collection, email=email, password=password)
    assert authenticated_user is None


def test_check_if_user_is_active(collection, new_user) -> None:
    created_user = crud.user.get(collection, new_user['_id'])
    is_active = crud.user.is_active(created_user)
    assert is_active is True


def test_check_if_user_is_inactive(collection) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password, is_active=False)
    user_id = crud.user.create(collection, document_in=user_in)

    created_user = crud.user.get(collection, user_id)
    is_active = crud.user.is_active(created_user)
    assert is_active is False


def test_check_if_user_is_superuser(collection) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = schemas.UserCreate(email=email, password=password, is_superuser=True)
    user_id = crud.user.create(collection, document_in=user_in)

    created_user = crud.user.get(collection, user_id)
    is_superuser = crud.user.is_superuser(created_user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(collection, new_user) -> None:
    created_user = crud.user.get(collection, new_user['_id'])
    is_superuser = crud.user.is_superuser(created_user)
    assert is_superuser is False
