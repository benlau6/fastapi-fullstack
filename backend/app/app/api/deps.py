from functools import lru_cache

from fastapi import Header, HTTPException, Depends

from app.core import config
from app.core.config import settings # immutable


############# settings ###########
@lru_cache
def get_settings():
    return config.Settings()


def get_db(settings: config.Settings = Depends(get_settings)):
    return None

    
##################################
# could be used for fine-grained control
async def verify_content_length(content_length: int = Header(...)):
    if content_length > settings.PAYLOAD_LIMIT:
        raise HTTPException(status_code=413, detail=f"Error, please make sure the files are smaller than {settings.PAYLOAD_LIMIT}")


async def verify_content_type(content_type: int = Header(...)):
    accepted_types = ['csv', 'png']
    if content_type not in accepted_types:
        raise HTTPException(status_code=..., detail=f"Incorrect file type")


async def verify_key(x_api_key: str = Header(...)):
    if x_api_key != "key":
        raise HTTPException(status_code=400, detail="X-Api-Key header invalid")


############ fastapi-users #############
from app.api.fastapi_users_utils import (
    get_current_user, 
    get_current_active_user, 
    get_current_active_verified_user,
    get_current_active_superuser,
)


########### fastapi-permission #########
from app.api.fastapi_permissions_utils import Permission
###############################