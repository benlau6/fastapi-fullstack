from typing import List
import secrets

from pydantic import BaseSettings


# env will be read in case-insensitive way by pydantic BaseSettings
# equal assignment assigns default value if there is no that env attribute
class Settings(BaseSettings):
    FILE_ROOT_PATH: str = '/data/fastapi/'
    ROOT_STR: str = '/api'
    API_V1_STR: str = '/v1'
    GRAPHQL_STR: str = '/graphql'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    TOKEN_RESOURCE_STR: str = '/auth/jwt/login'
    DATABASE_URL = "sqlite:///data/fastapi/dev.db"
    ###################
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    MONGO_URI: str = 'mongodb://admin:password@mongodb:27017'
    MONGO_DB_NAME: str = 'fastapi'
    MONGO_USER_COLLECTION_NAME: str = 'user'
    PAYLOAD_LIMIT: int = 2000000
    FIRST_SUPERUSER: str = 'admin@example.com'
    FIRST_SUPERUSER_PASSWORD: str = 'password'
    EMAIL_TEST_USER: str = 'test@example.com'
    EMAIL_TEST_USER_PASSWORD: str = 'password'
    USERS_OPEN_REGISTRATION: bool = True
    EMAIL_PROVIDER_RESTRICTION: bool = False
    ALLOWED_EMAIL_PROVIDER_LIST: List[str] = ['mtr', 'gmail', 'example', 'test']

    ############# scopes #############
    SCOPES_UPLOAD: List[str] = ['files:upload']
    SCOPES_DOWNLOAD: List[str] = ['files:download']

    #URL_DEFAULT_TTL=300
    #QUERY_DEFAULT_TTL=10
    #QUERY_CONCURRENT_LIMIT=10
    #QUERY_DEFAULT_WAITING_TIME=1
    #QUERY_DEFAULT_LIMIT_ROWS=1000

    # or it could read a env file
    class Config:
        env_file = '.env'

    @property
    def AUTH_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}/auth'

    @property
    def TOKEN_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}{self.TOKEN_RESOURCE_STR}'

    @property
    def USERS_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}/users'

settings = Settings()