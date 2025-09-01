from typing import Optional

from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    name: str
    email: str
    password: str


class UserUpdateDTO(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
