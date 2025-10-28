from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.config.types import RestaurantTableStatus


class RestorantTableDTO(BaseModel):
    id: int
    waiter_id: int
    status: RestaurantTableStatus = RestaurantTableStatus.AVAILABLE
    notes: Optional[str] = None
    # orders -> missing

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "status": "available",
                "waiter_id": 5,
                "notes": "VIP customer table near the window",
                "created_at": "2025-09-29T12:30:00Z",
                "updated_at": "2025-09-29T13:00:00Z",
                "deleted_at": None,
            }
        }


class RestoranTableCreateDTO(BaseModel):
    waiter_id: int
    status: RestaurantTableStatus = RestaurantTableStatus.AVAILABLE
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "waiter_id": 5,
                "status": "available",
                "notes": "VIP customer table near the window",
            }
        }


class UpdateRestorantTableDTO(BaseModel):
    number: Optional[int] = None
    waiter_id: Optional[int] = None
    status: Optional[RestaurantTableStatus] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "number": 15,
                "waiter_id": 3,
                "status": "occupied",
                "notes": "Change location to window",
            }
        }
