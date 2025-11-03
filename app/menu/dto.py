from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class MenuItemDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    available: bool = True
    category: Optional[str] = None

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Margherita Pizza",
                "description": "Classic pizza with tomato, mozzarella, and basil",
                "price": "12.50",
                "available": True,
                "category": "Pizza",
                "created_at": "2025-11-01T10:00:00Z",
                "updated_at": "2025-11-01T10:00:00Z",
                "deleted_at": None,
            }
        }


class CreateMenuItemDTO(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    available: bool = True
    category: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Margherita Pizza",
                "description": "Classic pizza with tomato, mozzarella, and basil",
                "price": "12.50",
                "available": True,
                "category": "Pizza",
            }
        }


class UpdateMenuItemDTO(BaseModel):
    description: Optional[str] = None
    price: Optional[Decimal] = None
    available: Optional[bool] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True
