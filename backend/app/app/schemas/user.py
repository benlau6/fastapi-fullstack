from bson.objectid import ObjectId
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, validator, constr
from app.schemas.utils import PyObjectId
from app.core.config import settings
from app.core.security import get_password_hash


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_superuser: bool = False
    # regex meaning
    # first str before ':' should only be in a-z, 0-9, -, _
    # second or after str after first ':' should only be in a-z, 0-9, -, _, @, . (think of email)
    # ':some_str' should appear at least 1, and can appear more than 1
    scopes: Optional[List[constr(regex=r'^[a-z0-9-_]+(:[a-z0-9-_@.]+)+$')]] = None
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
    
    ''' 
    You'll often want to use this together with pre, 
    since otherwise with always=True pydantic would try to validate the default None 
    which would cause an error.
    '''
    @validator('scopes', pre=True, always=True)
    def set_scopes(cls, v, values):
        if v is None:
            v = []
        default_scope = 'user:' + values['email']
        if default_scope not in v:
            v.append(default_scope)
        if values['is_superuser'] == True:
            v.append('role:admin')
        return v


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Additional properties stored in DB
class UserToDB(UserBase):
    hashed_password: str = Field(alias='password')

    class Config:
        allow_population_by_field_name=True
        response_model_by_alias=False
    
    @validator('hashed_password')
    def hash_password(cls, v):
        return get_password_hash(v)


# Additional properties to return via API
# not showing password or hashed_password
class UserFromDB(UserBase):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    class Config:
        allow_population_by_field_name = True
        response_model_by_alias=False
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# just for type check in crud
class UserInDB(UserToDB):
    _id: ObjectId


class UserCheckScopes(BaseModel):
    email: Optional[EmailStr] = None
    scopes: Optional[List[str]] = None


class UpdateResponse(BaseModel):
    matched_count: int 
    modified_count: int


class DeleteResponse(BaseModel):
    deleted_count: int