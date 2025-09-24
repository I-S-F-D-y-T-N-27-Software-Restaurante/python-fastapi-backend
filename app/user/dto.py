from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBaseDTO(BaseModel):
    id: int
    name: str
    email: EmailStr

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

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
    email: EmailStr
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
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

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
