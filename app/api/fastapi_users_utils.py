from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication, CookieAuthentication

from app.core.config import settings
from app.schemas import UserInDB, User, UserCreate, UserUpdate
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
    user_model=User,
    user_create_model=UserCreate,
    user_update_model=UserUpdate,
    user_db_model=UserInDB,
)


def on_after_register(user: UserInDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserInDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserInDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")