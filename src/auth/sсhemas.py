
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email : EmailStr
    phone : str | None = None
    full_name : str | None = None
    role: str = Field(..., description="customer | driver")
    is_active : bool = True


class UserCreate(UserBase):
    password : str


class UserUpdate(UserBase):
    email: EmailStr | None = None
    phone: str | None = None
    full_name: str | None = None
    role: str | None = None
    is_active: bool | None = None
    password: str | None = None


class UserRead(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserChangePassword(BaseModel):
    old_password: str
    new_password: str

class AuthToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshToken(BaseModel):
    token: str

