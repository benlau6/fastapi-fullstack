from typing import Any, Dict, List, Optional, Union
import secrets
import os

from pydantic import BaseSettings, validator


# env will be read in case-insensitive way by pydantic BaseSettings
# equal assignment assigns default value if there is no that env attribute
class Settings(BaseSettings):
    # Server path config
    FILE_ROOT_PATH: str = "/data/files/"
    # MONGO
    MONGO_USER: str = "admin"
    MONGO_PASSWORD: str = "password"
    MONGO_SERVER: str = "mongodb"
    MONGO_PORT: str = "27017"
    # MONGO DATA
    MONGO_DB_NAME: str = "fastapi"
    # SQL
    SQLITE_FILE_NAME: str = "dev.db"
    # API path
    ROOT_STR: str = "/api"
    API_V1_STR: str = "/v1"
    TOKEN_RESOURCE_STR: str = "/login/access-token"
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # user init
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "password"
    FIRST_NORMAL_USER: str = "user@example.com"
    FIRST_NORMAL_USER_PASSWORD: str = "password"
    # user related
    USERS_OPEN_REGISTRATION: bool = True
    EMAIL_PROVIDER_RESTRICTION: bool = True
    ALLOWED_EMAIL_PROVIDER_LIST: List[str] = ["gmail", "example", "test"]
    # limit
    PAYLOAD_LIMIT: int = 2000000
    # URL_DEFAULT_TTL=300
    # QUERY_DEFAULT_TTL=10
    # QUERY_CONCURRENT_LIMIT=10
    # QUERY_DEFAULT_WAITING_TIME=1
    # QUERY_DEFAULT_LIMIT_ROWS=1000
    # scopes
    SCOPES_UPLOAD: List[str] = ["files:upload"]
    SCOPES_DOWNLOAD: List[str] = ["files:download"]

    # it could read a env file
    # class Config:
    #    env_file = '.env'

    @property
    def SQLITE_URI(self) -> str:
        # 4 slashes for absolute path
        return f"sqlite:////data/db/{self.SQLITE_FILE_NAME}"

    @property
    def MONGO_URI(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_SERVER}:{self.MONGO_PORT}"

    @property
    def AUTH_URL(self) -> str:
        return f"{self.ROOT_STR}{self.API_V1_STR}/auth"

    @property
    def TOKEN_URL(self) -> str:
        return f"{self.AUTH_URL}{self.TOKEN_RESOURCE_STR}"

    @property
    def TOKEN_TEST_URL(self) -> str:
        return f"{self.AUTH_URL}/test-token"

    @property
    def USERS_URL(self) -> str:
        return f"{self.ROOT_STR}{self.API_V1_STR}/users"

    @property
    def DOWNLOAD_URL(self) -> str:
        return f"{self.ROOT_STR}{self.API_V1_STR}/download"

    @property
    def UPLOAD_URL(self) -> str:
        return f"{self.ROOT_STR}{self.API_V1_STR}/upload"


settings = Settings()
