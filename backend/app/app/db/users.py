from fastapi_users.db import TortoiseUserDatabase

from app import schemas, models

user_db = TortoiseUserDatabase(schemas.UserInDB, models.UserModel)
