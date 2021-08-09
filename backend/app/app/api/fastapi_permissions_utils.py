from fastapi import Depends
from fastapi_permissions import configure_permissions
from fastapi_permissions import Authenticated, Everyone

from app import schemas
from app.api.fastapi_users_utils import (
    get_current_user, 
    get_current_active_user, 
    get_current_active_verified_user,
    get_current_active_superuser,
)

def get_current_active_user_principals(current_user: schemas.User = Depends(get_current_active_user)):
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