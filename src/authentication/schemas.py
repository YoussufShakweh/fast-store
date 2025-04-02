import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    model_config = {"from_attributes": True}

    @field_validator("first_name")
    def validate_first_name(cls, v: str):
        if not re.fullmatch(r"^[A-Za-z]+$", v):
            raise ValueError("First name must contain only alphabetic letters")

        return v.capitalize()

    @field_validator("last_name")
    def validate_last_name(cls, v: str):
        if not re.fullmatch(r"^[A-Za-z]+$", v):
            raise ValueError("Last name must contain only alphabetic letters")

        return v.capitalize()


class UserList(BaseUser):
    id: int


class UserCreate(BaseUser):
    password: str
    is_active: bool = True
    is_superuser: bool = False

    @field_validator("password")
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        return v


class UserDetail(BaseUser):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    first_name: str | None = ...
    last_name: str | None = ...
    email: EmailStr | None = ...
    is_active: bool | None = ...
    is_superuser: bool | None = ...

    model_config = {"from_attributes": True}
