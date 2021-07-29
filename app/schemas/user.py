from typing import List, Optional

from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel, TortoiseUserDatabase
from tortoise.contrib.pydantic import PydanticModel

class UserModel(TortoiseBaseUserModel):
    pass


class User(models.BaseUser):
    principals: Optional[List[str]] = None


class UserCreate(models.BaseUserCreate):
    principals: Optional[List[str]] = None
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserInDB(User, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = UserModel
