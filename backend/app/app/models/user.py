from fastapi_users.db import TortoiseBaseUserModel
from tortoise import fields


class UserModel(TortoiseBaseUserModel):
    principals = fields.JSONField() 
