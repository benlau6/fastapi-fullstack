from typing import List, Optional

from fastapi_users.db import TortoiseBaseUserModel, TortoiseUserDatabase

from app.schemas import UserInDB


class UserModel(TortoiseBaseUserModel):
    pass


user_db = TortoiseUserDatabase(UserInDB, UserModel)
