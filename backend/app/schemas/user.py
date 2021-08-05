from typing import List, Optional, Any

import pydantic
from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel

import app.models as app_models


class User(models.BaseUser):
    principals: Optional[List[str]] = None

    @pydantic.root_validator
    def principals_set_config(cls, values):
        principals = values.get('principals')
        email = values.get('email')
        if principals is None:
            values["principals"] = ['user:' + email]
        return values


class UserCreate(models.BaseUserCreate):
    principals: Optional[List[str]] = None


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserInDB(User, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = app_models.UserModel
