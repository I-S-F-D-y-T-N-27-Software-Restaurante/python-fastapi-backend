from typing import Optional

from pydantic import BaseModel

from app.modules.resto.entities import Admin, Cashier, Cook, Waiter
from app.shared.timestamp_mixin import TimestampMixin


class User(BaseModel):
    name: str
    email: str
    password: str


class UserEntity(User, TimestampMixin):
    id: int

    waiter_profile: Optional["Waiter"] = None
    cook_profile: Optional["Cook"] = None
    cashier_profile: Optional["Cashier"] = None
    admin_profile: Optional["Admin"] = None
