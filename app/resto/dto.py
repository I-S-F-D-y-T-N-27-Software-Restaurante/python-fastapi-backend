from __future__ import annotations

from datetime import datetime
from typing import Optional

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
    # deleted_at: datetime | None = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 10,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "created_at": "2025-09-24T11:30:00Z",
                "updated_at": "2025-09-24T11:40:00Z",
                "deleted_at": None,
                "waiter_profile": {"id": 1, "user_id": 10},
                "cashier_profile": {"id": 2, "user_id": 10},
                "cook_profile": {"id": 3, "user_id": 10},
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


class RestorantTableDTO(BaseModel):
    id: int
    number: int
    waiter_id: int
    order_status_id: int
    occupied: bool = False
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "number": 12,
                "waiter_id": 5,
                "order_status_id": 2,
                "occupied": True,
                "notes": "VIP customer table near the window",
                "created_at": "2025-09-29T12:30:00Z",
                "updated_at": "2025-09-29T13:00:00Z",
                "deleted_at": None,
            }
        }


class RestoranTableCreateDTO(BaseModel):
    number: int
    waiter_id: int
    order_status_id: int
    occupied: bool = False
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "number": 12,
                "waiter_id": 5,
                "order_status_id": 2,
                "occupied": True,
                "notes": "VIP customer table near the window",
            }
        }


class UpdateRestorantTableDTO(BaseModel):
    number: Optional[int] = None
    waiter_id: Optional[int] = None
    order_status_id: Optional[int] = None
    occupied: Optional[bool] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "number": 15,
                "waiter_id": 3,
                "order_status_id": 4,
                "occupied": False,
                "notes": "Change location to window",
            }
        }
