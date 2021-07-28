from typing import Any, Dict, Optional, Union

from app.crud.base import CRUDBase

from app.models.user import UserCreate, UserUpdate, UserInDB

from app.api.fastapi_users_utils import fastapi_users

class CRUDUser(CRUDBase[Dict, UserCreate, UserUpdate]):
    
    async def get_by_email(self, db, email: str) -> Optional[Dict]:
        user = await fastapi_users.get_user(email)
        return user

    async def create(self, db, obj_in):
        user = await fastapi_users.create_user(obj_in) 
        return user

    def is_verified(self, user: Dict) -> bool:
        return user['is_verified']

    def is_active(self, user: Dict) -> bool:
        return user['is_active']

    def is_superuser(self, user: Dict) -> bool:
        return user['is_superuser']


user = CRUDUser(UserInDB)