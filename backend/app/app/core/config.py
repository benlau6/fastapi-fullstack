from typing import List
import secrets

from pydantic import BaseSettings


# env will be read in case-insensitive way by pydantic BaseSettings
# equal assignment assigns default value if there is no that env attribute
class Settings(BaseSettings):
    ########## Server path config ###########
    FILE_ROOT_PATH: str = '/data/files/'
    DATABASE_URL: str = "sqlite:///data/db/dev.db"
    ########## API path #############
    ROOT_STR: str = '/api'
    API_V1_STR: str = '/v1'
    GRAPHQL_STR: str = '/graphql'
    TOKEN_RESOURCE_STR: str = '/auth/jwt/login'
    ################################
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ############# user init ##############
    FIRST_SUPERUSER: str = 'admin@gmail.com'
    FIRST_NORMAL_USER: str = 'user@gmail.com'
    ############# limit #############
    PAYLOAD_LIMIT: int = 2000000
    #URL_DEFAULT_TTL=300
    #QUERY_DEFAULT_TTL=10
    #QUERY_CONCURRENT_LIMIT=10
    #QUERY_DEFAULT_WAITING_TIME=1
    #QUERY_DEFAULT_LIMIT_ROWS=1000
    #EMAIL_PROVIDER_RESTRICTION: bool = False
    #ALLOWED_EMAIL_PROVIDER_LIST: List[str] = ['mtr', 'gmail', 'example', 'test']
    ############# scopes #############
    #SCOPES_UPLOAD: List[str] = ['files:upload']
    #SCOPES_DOWNLOAD: List[str] = ['files:download']

    # it could read a env file
    #class Config:
    #    env_file = '.env'

    @property
    def AUTH_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}/auth'

    @property
    def TOKEN_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}{self.TOKEN_RESOURCE_STR}'

    @property
    def USERS_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}/users'

    @property
    def DOWNLOAD_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}/download'

    @property
    def UPLOAD_URL(self) -> str:
        return f'{self.ROOT_STR}{self.API_V1_STR}/upload'


settings = Settings()