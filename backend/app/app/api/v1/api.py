from fastapi import Depends, FastAPI
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from fastapi_permissions import Allow, Deny, All, Authenticated, Everyone

from app import schemas
from app.core.config import settings
from app.api import deps
from app.api.v1.endpoints import upload, download, users
from app.api.fastapi_users_utils import (
    fastapi_users_instance, 
    jwt_authentication, 
    cookie_authentication,
    on_after_register, 
    on_after_forgot_password,
    after_verification_request
)
from app.api.fastapi_permissions_utils import Permission

# fastapi-permission
upload_acl = [
    (Allow, Authenticated, "view"),
    (Allow, 'role:admin', All)
]

download_acl = [
    (Allow, Authenticated, "view"),
    (Allow, 'role:admin', All)
]

potato_acl = [
    (Allow, Authenticated, "view"),
    (Allow, 'role:admin', All)
]

# to include router
api_v1 = FastAPI()

api_v1.include_router(
    users.router, prefix='/users', tags=['users']
)

api_v1.include_router(
    CRUDRouter(schema=schemas.Potato), dependencies=[Permission('view', potato_acl)]
)

api_v1.include_router(
    upload.router, prefix='/upload', tags=['upload'], dependencies=[Permission('view', upload_acl)]
)

api_v1.include_router(
    download.router, prefix='/download', tags=['download'], dependencies=[Permission('view', download_acl)]
)

# fastapi-users
api_v1.include_router(
    fastapi_users_instance.get_users_router(), prefix="/users", tags=["users"]
)

api_v1.include_router(
    fastapi_users_instance.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

api_v1.include_router(
    fastapi_users_instance.get_auth_router(cookie_authentication), prefix="/auth/cookie", tags=["auth"]
)

api_v1.include_router(
    fastapi_users_instance.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

api_v1.include_router(
    fastapi_users_instance.get_reset_password_router(
        settings.SECRET_KEY, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)

api_v1.include_router(
    fastapi_users_instance.get_verify_router(
        settings.SECRET_KEY, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)
