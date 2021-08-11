from fastapi import FastAPI, Depends, Security
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from fastapi_permissions import Allow, Deny, All, Authenticated, Everyone

from app import schemas
from app.core.config import settings
from app.api import deps
from app.api.deps import ActiveUserPermission
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

potato_acl = [
    (Allow, Authenticated, "view"),
    (Allow, 'role:admin', All)
]

# to include router
api_v1 = FastAPI()

api_v1.include_router(login.router, prefix='/login', tags=['login'])
api_v1.include_router(users.router, prefix='/users', tags=['users'])

api_v1.include_router(
    CRUDRouter(schema=schemas.Potato), dependencies=[ActiveUserPermission('view', potato_acl)]
    )

api_v1.include_router(
    upload.router, 
    prefix='/upload', 
    tags=['upload'], 
    dependencies=[
        Security(deps.get_current_active_user, scopes=settings.SCOPES_DOWNLOAD),
        ActiveUserPermission('view', upload_acl),
        ]
    )

api_v1.include_router(
    download.router, 
    prefix='/download', 
    tags=['download'], 
    dependencies=[
        Security(deps.get_current_active_user, scopes=settings.SCOPES_UPLOAD),
        ActiveUserPermission('view', download_acl)
        ]
    )
