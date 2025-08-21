from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    is_active: Optional[bool] = True
    user_category: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserCreateWithOracle(BaseModel):
    user: UserCreate
    oracle_username: str
    oracle_password: str

class UserResponse(UserBase):
    id: int
    guid: Optional[str]
    class Config:
        orm_mode = True

class LogResponse(BaseModel):
    id: int
    action: str
    username: Optional[str]
    status: str
    message: Optional[str]
    timestamp: datetime
    class Config:
        orm_mode = True

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        orm_mode = True 