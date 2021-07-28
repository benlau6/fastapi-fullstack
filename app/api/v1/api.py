from fastapi import APIRouter, Depends
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter


from app import schemas
from app.core.config import settings
from app.api import deps
from app.api.v1.endpoints import upload, download
from app.api.fastapi_users_utils import (
    fastapi_users, 
    jwt_authentication, 
    cookie_authentication,
    on_after_register, 
    on_after_forgot_password,
    after_verification_request
)


router = APIRouter()
router.include_router(upload.router, prefix='/upload', tags=['upload'], dependencies=[Depends(deps.get_current_active_user)])
router.include_router(download.router, prefix='/download', tags=['download'], dependencies=[Depends(deps.get_current_active_user)])
router.include_router(CRUDRouter(schema=schemas.Potato))

## fastapi-users
router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

router.include_router(
    fastapi_users.get_auth_router(cookie_authentication), prefix="/auth/cookie", tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

router.include_router(
    fastapi_users.get_reset_password_router(
        settings.SECRET_KEY, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_verify_router(
        settings.SECRET_KEY, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)
