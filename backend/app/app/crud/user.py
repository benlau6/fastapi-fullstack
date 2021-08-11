from typing import Any, Dict, Optional, Union

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase

from app.schemas.user import UserCreate, UserUpdate, UserToDB


class CRUDUser(CRUDBase[Dict, UserCreate, UserUpdate]):
    
    def get_by_email(self, collection, *, email: str) -> Optional[Dict]:
        user = collection.find_one({'email': email})
        return user

    def authenticate(self, collection, *, email: str, password: str) -> Optional[Dict]:
        user = self.get_by_email(collection, email=email)
        if not user:
            return None
        if not verify_password(password, user['hashed_password']):
            return None
        return user

    def is_active(self, user: Dict) -> bool:
        return user['is_active']

    def is_superuser(self, user: Dict) -> bool:
        return user['is_superuser']


user = CRUDUser(UserToDB)