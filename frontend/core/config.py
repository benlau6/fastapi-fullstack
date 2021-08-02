from typing import List

from pydantic import BaseSettings


# env will be read in case-insensitive way by pydantic BaseSettings
# equal assignment assigns default value if there is no that env attribute
class Settings(BaseSettings):
    ########## Server path config ###########
    ########## API path #############
    ROOT_STR: str = '/api'
    API_V1_STR: str = '/v1'
    GRAPHQL_STR: str = '/graphql'
    TOKEN_RESOURCE_STR: str = '/auth/jwt/login'
    ################################

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