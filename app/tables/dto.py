from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TableBaseDTO(BaseModel):
    number: int
    waiter_id: Optional[int] = None
    order_status_id: Optional[int] = None
    occupied: Optional[bool] = False
    notes: Optional[str] = None

class TableCreateDTO(TableBaseDTO):
    pass

class TableUpdateDTO(BaseModel):
    waiter_id: Optional[int] = None
    order_status_id: Optional[int] = None
    occupied: Optional[bool] = None
    notes: Optional[str] = None

class TableResponseDTO(TableBaseDTO):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True