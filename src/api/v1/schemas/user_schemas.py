from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    first_name: str
    last_name: str
    email: str


class UserDetailResponse(UserResponse):
    created_at: datetime | None = None
    updated_at: datetime | None = None
