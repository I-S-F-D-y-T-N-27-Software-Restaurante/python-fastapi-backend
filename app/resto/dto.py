from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBaseWithRestoProfilesDTO(BaseModel):
    id: int
    name: str
    email: EmailStr

    waiter_profile: WaiterBaseDTO | None = None
    cashier_profile: CashierBaseDTO | None = None
    cook_profile: CookBaseDTO | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 10,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "waiter_profile": {"id": 1, "user_id": 10},
                "cashier_profile": {"id": 2, "user_id": 10},
                "cook_profile": {"id": 3, "user_id": 10},
                "created_at": "2025-09-24T11:30:00Z",
                "updated_at": "2025-09-24T11:40:00Z",
            }
        }


class WaiterBaseDTO(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {"example": {"id": 1, "user_id": 10}}


class CashierBaseDTO(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {"example": {"id": 2, "user_id": 10}}


class CookBaseDTO(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {"example": {"id": 3, "user_id": 10}}
