from fastapi_users.db import TortoiseUserDatabase
from app.schemas import UserInDB
from app.models import UserModel

user_db = TortoiseUserDatabase(UserInDB, UserModel)
