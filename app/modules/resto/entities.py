from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from app.shared.timestamp_mixin import TimestampMixin


class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(kw_only=True)
class Table:
    number: int
    waiter_id: int
    customer_id: Optional[int] = None
    order_time: Optional[datetime] = None
    order_status: Optional[OrderStatus] = None
    occupied: bool = False
    notes: Optional[str] = None

    id: Optional[int] = None


@dataclass(kw_only=True)
class TableEntity(Table, TimestampMixin):
    pass


@dataclass(kw_only=True)
class Order:
    table_id: int
    waiter_id: int
    status: Optional[OrderStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total: Optional[float] = None
    notes: Optional[str] = None

    id: Optional[int] = None


@dataclass(kw_only=True)
class OrderEntity(Order, TimestampMixin):
    pass


@dataclass(kw_only=True)
class OrderItem:
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: float
    notes: Optional[str] = None

    id: Optional[int] = None


@dataclass(kw_only=True)
class OrderItemEntity(OrderItem, TimestampMixin):
    pass


class PaymentMethod(str, Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    TRANSFER = "transfer"


@dataclass(kw_only=True)
class Payment:
    order_id: int
    cashier_id: int
    payment_method: PaymentMethod
    amount: float
    payment_time: Optional[datetime] = None
    notes: Optional[str] = None
    discounts_applied: Optional[int] = None

    id: Optional[int] = None


@dataclass(kw_only=True)
class PaymentEntity(Payment, TimestampMixin):
    pass
