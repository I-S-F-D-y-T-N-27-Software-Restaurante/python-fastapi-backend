from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WaiterProfile(BaseModel):
    id: int

    class Config:
        from_attributes = True


class CookProfile(BaseModel):
    id: int

    class Config:
        from_attributes = True


class CashierProfile(BaseModel):
    id: int

    class Config:
        from_attributes = True


class UserWithProfiles(User):
    waiter_profile: Optional["WaiterProfile"] = None
    cook_profile: Optional["CookProfile"] = None
    cashier_profile: Optional["CashierProfile"] = None
