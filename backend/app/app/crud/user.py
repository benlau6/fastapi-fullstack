from typing import Any, Dict, Optional, Union

from app import schemas
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[schemas.UserInDB, schemas.UserCreate, schemas.UserUpdate]):
    
    def get_by_email(self, collection, email: str) -> Optional[schemas.UserInDB]:
        user = collection.find_one({'email': email})
        return user

    def authenticate(self, collection, email: str, password: str) -> Optional[schemas.UserInDB]:
        user = self.get_by_email(collection, email=email)
        if not user:
            return None
        if not verify_password(password, user['hashed_password']):
            return None
        return user

    def is_active(self, user: schemas.UserInDB) -> bool:
        return user['is_active']

    def is_superuser(self, user: schemas.UserInDB) -> bool:
        return user['is_superuser']


user = CRUDUser(schemas.UserToDB)