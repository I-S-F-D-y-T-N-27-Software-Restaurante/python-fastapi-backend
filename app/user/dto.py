from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBaseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr  # Cambiado de 'emails' a 'email'

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "created_at": "2025-09-24T11:30:00Z",
                "updated_at": "2025-09-24T11:40:00Z",
                "deleted_at": None,
            }
        }
        str_strip_whitespace = True


class UserCreateDTO(BaseModel):
    name: str
    email: EmailStr  # Cambiado de 'emails'
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Bob Smith",
                "email": "bob@example.com",
                "password": "securepassword123",
            }
        }
        str_strip_whitespace = True


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None  # Cambiado
    password: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Updated Name",
                "email": "updated@example.com",
                "password": "newsecurepassword456",
            }
        }


class UserDeleteDTO(BaseModel):
    id: int
    name: str
    email: EmailStr
    deleted_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "deleted_at": "2025-09-24T12:00:00Z",
            }
        }


class UserLoginDTO(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {"email": "alice@example.com", "password": "pass123"}
        }


class TokenDTO(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    user_email: str
    roles: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "user_email": "alice@example.com",
                "roles": ["admin", "waiter"],
            }
        }


class UserTokenDataDTO(BaseModel):
    user_id: str
    user_email: str
    roles: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "user_email": "alice@example.com",
                "roles": ["admin", "waiter"],
            }
        }
