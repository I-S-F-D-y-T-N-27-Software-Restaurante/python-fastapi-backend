from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional , List

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

class OrderItemBaseDTO(BaseModel):
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class OrderItemDTO(OrderItemBaseDTO):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderBaseDTO(BaseModel):
    table_id: int
    waiter_id: int
    status_id: int
    total: Decimal
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class OrderCreateDTO(OrderBaseDTO):
    items: List[OrderItemBaseDTO]  # incluir ítems al crear el pedido


class OrderDTO(OrderBaseDTO):
    id: int
    items: List[OrderItemDTO]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 15,
                "table_id": 3,
                "waiter_id": 5,
                "status_id": 1,
                "total": "1250.50",
                "notes": "Sin hielo en las bebidas",
                "items": [
                    {
                        "id": 1,
                        "menu_item_id": 8,
                        "quantity": 2,
                        "unit_price": "350.00",
                        "notes": "Sin cebolla",
                        "created_at": "2025-10-19T15:30:00Z",
                        "updated_at": "2025-10-19T15:35:00Z",
                    }
                ],
                "created_at": "2025-10-19T15:30:00Z",
                "updated_at": "2025-10-19T15:35:00Z",
                "deleted_at": None,
            }
        }