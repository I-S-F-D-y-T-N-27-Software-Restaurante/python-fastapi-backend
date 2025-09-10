from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserResponseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdateDTO(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
