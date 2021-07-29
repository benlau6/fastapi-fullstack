from functools import lru_cache

from fastapi import Header, HTTPException, Depends

from app import schemas
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
from app.api.fastapi_users_utils import fastapi_users_instance


get_current_user = fastapi_users_instance.current_user()

get_current_active_user = fastapi_users_instance.current_user(active=True)

get_current_active_verified_user = fastapi_users_instance.current_user(active=True, verified=True)

get_current_active_superuser = fastapi_users_instance.current_user(active=True, superuser=True)

########### fastapi-permission #########
from fastapi_permissions import configure_permissions
from fastapi_permissions import Authenticated, Everyone


def get_current_active_user_principals(current_user: schemas.User = Depends(get_current_user)):
    if current_user is not None:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.extend(getattr(current_user, "principals", []))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals

# Permission is already wrapped in Depends()
Permission = configure_permissions(get_current_active_user_principals)
###############################