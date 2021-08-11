  
from app import crud


def test_created_user_exists(new_user_id):
    found_user = crud.user.get(new_user_id)
    assert found_user is not None
    assert found_user.email == new_user.email
    assert found_user.principals == new_user.principals


def test_users_exists(client, settings, superuser_token_headers):
    r = client.get(f'{settings.USERS_URL}', headers=superuser_token_headers)
    all_users = r.json()
    assert len(all_users) >= 2