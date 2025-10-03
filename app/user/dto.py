from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class TaskSimple(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    state: str
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: str  # Cambiado de 'emails' a 'email'
    ages: int

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
        
class UserOut(UserBase):
    id: str
    tasks: List[TaskSimple] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "firstName": "John",
                "lastName": "Doe",
                "email": "admin@sistema.com",  # Cambiado
                "ages": 30,
                "tasks": [
                    {
                        "id": 1,
                        "title": "Implementar autenticación",
                        "description": "Desarrollar sistema de login con JWT",
                        "state": "pending"
                    }
                ]
            }
        }

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
    email: EmailStr  # Cambiado
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
        

class UserLogin(BaseModel):
    email: str  # Cambiado de 'emails'
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@sistema.com",
                "password": "admin123"
            }
        }


class UserInsertDTO(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str  # Cambiado
    password: str
    ages: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "firstName": "John",
                "lastName": "Doe",
                "email": "admin@sistema.com",  # Cambiado
                "password": "hashedPassword123",
                "ages": 30
            }
        }
        

class UserUpdateDTO (UserBase):
    password: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe", 
                "email": "admin@sistema.com",  # Cambiado
                "password": "myNewPassword456",
                "ages": 30
            }
        }
        
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    user_email: str  

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user_id": "fb2e3fd3-12f2-4173-b9a2-ec57e4d39c36",
                "user_email": "admin@sistema.com"
            }
        }