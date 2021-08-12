from fastapi import APIRouter, Depends, Security
from fastapi_permissions import Allow, Deny, All, Authenticated, Everyone

from app import schemas
from app.core.config import settings
from app.api import deps
from app.api.deps import Permission
from app.api.v1.endpoints import upload, download, users, login


# fastapi-permission
upload_acl = [
    (Allow, Authenticated, "view"),
    (Allow, 'role:admin', All)
]

download_acl = [
    (Allow, Authenticated, "view"),
    (Allow, 'role:admin', All)
]

router = APIRouter(prefix='/v1')

router.include_router(login.router, prefix='/login', tags=['login'])
router.include_router(users.router, prefix='/users', tags=['users'])

router.include_router(
    upload.router, 
    prefix='/upload', 
    tags=['upload'], 
    dependencies=[
        Security(deps.get_current_active_user, scopes=settings.SCOPES_UPLOAD),
        ]
    )

router.include_router(
    download.router, 
    prefix='/download', 
    tags=['download'], 
    dependencies=[
        Security(deps.get_current_active_user, scopes=settings.SCOPES_DOWNLOAD),
        ]
    )
