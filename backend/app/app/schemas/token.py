from typing import Optional, List

from pydantic import BaseModel, constr

from app.schemas.utils import Scope


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    scopes: List[Scope]