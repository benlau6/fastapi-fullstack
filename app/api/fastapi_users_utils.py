from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication, CookieAuthentication

from app.core.config import settings
from app import schemas
from app.db import user_db


jwt_authentication = JWTAuthentication(
    secret=settings.SECRET_KEY, 
    lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES//60, 
    tokenUrl=settings.TOKEN_URL
)

cookie_authentication = CookieAuthentication(
    secret=settings.SECRET_KEY,
    lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES//60,
)

fastapi_users_instance = FastAPIUsers(
    db=user_db,
    auth_backends=[jwt_authentication, cookie_authentication],
    user_model=schemas.User,
    user_create_model=schemas.UserCreate,
    user_update_model=schemas.UserUpdate,
    user_db_model=schemas.UserInDB,
)


def on_after_register(user: schemas.UserInDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: schemas.UserInDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: schemas.UserInDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


get_current_user = fastapi_users_instance.current_user()

get_current_active_user = fastapi_users_instance.current_user(active=True)

get_current_active_verified_user = fastapi_users_instance.current_user(active=True, verified=True)

get_current_active_superuser = fastapi_users_instance.current_user(active=True, superuser=True)