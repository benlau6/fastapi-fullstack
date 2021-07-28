from bson.objectid import ObjectId
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator
from app.schemas.utils import PyObjectId
from app.core.config import settings
from app.core.security import get_password_hash


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    scopes: Optional[List[str]] = None
    full_name: Optional[str] = None
    contact_number: Optional[str] = None

    @validator('email')
    def email_validate_provider(cls, v):
        if settings.EMAIL_PROVIDER_RESTRICTION:
            if not any(provider in v for provider in settings.ALLOWED_EMAIL_PROVIDER_LIST):
                raise ValueError("Invalid email provider")
        return v

    @property
    def short_name(self) -> str:
        return self.email.split('@')[0]


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    scopes: List[str] = ['me']


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    class Config:
        allow_population_by_field_name = True
        response_model_by_alias=False
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str = Field(alias='password')

    class Config:
        allow_population_by_field_name=True
        response_model_by_alias=False
    
    @validator('hashed_password')
    def hash_password(cls, v):
        return get_password_hash(v)


# Additional properties to return via API
# not showing password or hashed_password
class User(UserInDBBase):
    pass


class UserCheckScopes(BaseModel):
    email: Optional[EmailStr] = None
    scopes: Optional[List[str]] = None




## Shared properties
#class UserBase(BaseModel):
#    email: Optional[EmailStr] = None
#    is_active: Optional[bool] = True
#    is_superuser: bool = False
#    full_name: Optional[str] = None
#
#
## Properties to receive via API on creation
#class UserCreate(UserBase):
#    email: EmailStr
#    password: str
#
#
## Properties to receive via API on update
#class UserUpdate(UserBase):
#    password: Optional[str] = None
#
#
#class UserInDBBase(UserBase):
#    id: Optional[int] = None
#
#
## Additional properties to return via API
#class User(UserInDBBase):
#    pass
#
#
## Additional properties stored in DB
#class UserInDB(UserInDBBase):
#    hashed_password: str