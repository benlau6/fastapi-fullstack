from fastapi import Depends, FastAPI
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter
from fastapi_permissions import Allow, Deny, All, Authenticated, Everyone

from app import schemas
from app.core.config import settings
from app.api import deps
from app.api.v1.endpoints import upload, download, users
from app.api.deps import Permission

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
