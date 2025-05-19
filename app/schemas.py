from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: str
    username: str
    fullname: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    email: str