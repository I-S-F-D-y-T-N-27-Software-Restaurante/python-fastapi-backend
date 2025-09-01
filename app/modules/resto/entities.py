from typing import List, Optional

from pydantic import BaseModel

from app.modules.user.entities import User
from app.shared.timestamp_mixin import TimestampMixin


class Waiter(BaseModel):
    id: int
    user: User
    tables: List["Table"] = []
    orders: List["Order"] = []


class Cook(BaseModel):
    id: int
    user: User
    preparations: List["Preparation"] = []


class Cashier(BaseModel):
    id: int
    user: User
    payments: List["Payment"] = []


class Table(BaseModel):
    id: int
    number: int
    waiter_id: int
    order_status_id: int
    occupied: bool
    notes: Optional[str] = None
    waiter: Optional[Waiter] = None
    order_status: Optional["OrderStatus"] = None
    orders: List["Order"] = []


class TableEntity(Table, TimestampMixin):
    pass


class Preparation(BaseModel):
    id: int
    order_item_id: int
    cook_id: int
    status_id: int
    cancelled: bool
    cancellation_reason: Optional[str] = None
    order_item: Optional["OrderItem"] = None
    cook: Optional[Cook] = None
    status: Optional["OrderStatus"] = None


class OrderStatus(BaseModel):
    id: int
    name: str
    tables: List[Table] = []
    orders: List["Order"] = []
    preparations: List[Preparation] = []


class Order(BaseModel):
    id: int
    table_id: int
    waiter_id: int
    status_id: int
    total: float
    notes: Optional[str] = None
    table: Optional[Table] = None
    waiter: Optional[Waiter] = None
    status: Optional[OrderStatus] = None
    items: List["OrderItem"] = []
    payments: List["Payment"] = []
    invoice: Optional["Invoice"] = None


class OrderItem(BaseModel):
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    unit_price: float
    notes: Optional[str] = None
    order: Optional[Order] = None
    menu_item: Optional["MenuItem"] = None
    preparations: List[Preparation] = []


class MenuItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    available: bool
    category: Optional[str] = None


class Payment(BaseModel):
    id: int
    order_id: int
    cashier_id: int
    method_id: int
    amount: float
    payment_time: Optional[str] = None
    notes: Optional[str] = None
    discounts_applied: Optional[int] = None
    order: Optional[Order] = None
    cashier: Optional[Cashier] = None
    method: Optional["PaymentMethod"] = None


class PaymentMethod(BaseModel):
    id: int
    name: str
    payments: List[Payment] = []


class Invoice(BaseModel):
    id: int
    order_id: int
    issuer_id: int
    invoice_number: str
    issue_date: Optional[str] = None
    total_amount: float
    details: Optional[str] = None
    order: Optional[Order] = None


class Admin(BaseModel):
    id: int
    user: User
    audits: List["Audit"] = []


class Audit(BaseModel):
    id: int
    admin_id: int
    action: str
    description: Optional[str] = None
    date: Optional[str] = None
    affected_entity: str
    entity_id: int
    admin: Optional[Admin] = None
