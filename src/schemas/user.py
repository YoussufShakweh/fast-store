import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = ...
    password: str = Field(..., min_length=7, max_length=128)


class UserData(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    is_superuser: bool

    model_config = {"from_attributes": True}


class UserList(BaseModel):
    count: int
    data: list[UserData]


class UserDetail(UserData):
    last_login: datetime | None
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
