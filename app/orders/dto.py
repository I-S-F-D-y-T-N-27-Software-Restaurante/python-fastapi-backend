from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class CreateOrderDTO(BaseModel):
    waiter_id: int
    table_id: int
    total: Decimal
    menu_item_ids: list[int]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "waiter_id": 3,
                "table_id": 7,
                "total": 2560.75,
                "menu_item_ids": [1, 4, 6],
            }
        }
