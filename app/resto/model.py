from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.basemodel import Base
from app.config.types import TimestampMixin

if TYPE_CHECKING:
    from app.payment.model import Invoice, Payment
    from app.user.model import User


class Waiter(Base):
    __tablename__ = "waiters"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped[User] = relationship("User", back_populates="waiter_profile")

    tables: Mapped[list[Table]] = relationship("Table", back_populates="waiter")
    orders: Mapped[list[Order]] = relationship("Order", back_populates="waiter")


class Table(Base, TimestampMixin):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(nullable=False)

    waiter_id: Mapped[int] = mapped_column(ForeignKey("waiters.id"))
    order_status_id: Mapped[int] = mapped_column(ForeignKey("order_statuses.id"))

    occupied: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    waiter: Mapped[Waiter] = relationship("Waiter", back_populates="tables")
    order_status: Mapped["OrderStatus"] = relationship(
        "OrderStatus", back_populates="tables"
    )
    orders: Mapped[list[Order]] = relationship("Order", back_populates="table")


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    waiter_id: Mapped[int] = mapped_column(ForeignKey("waiters.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("order_statuses.id"))

    total: Mapped[DECIMAL] = mapped_column(DECIMAL)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    table: Mapped[Table] = relationship("Table", back_populates="orders")
    waiter: Mapped[Waiter] = relationship("Waiter", back_populates="orders")
    status: Mapped[OrderStatus] = relationship("OrderStatus", back_populates="orders")
    items: Mapped[list[OrderItem]] = relationship("OrderItem", back_populates="order")
    payments: Mapped[list[Payment]] = relationship("Payment", back_populates="order")
    invoice: Mapped[Invoice] = relationship(
        "Invoice", back_populates="order", uselist=False
    )


class Cook(Base):
    __tablename__ = "cooks"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped[User] = relationship("User", back_populates="cook_profile")

    preparations: Mapped[list["Preparation"]] = relationship(
        "Preparation", back_populates="cook"
    )


class Preparation(Base, TimestampMixin):
    __tablename__ = "preparations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_items.id"))
    cook_id: Mapped[int] = mapped_column(ForeignKey("cooks.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("order_statuses.id"))

    cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    order_item: Mapped[OrderItem] = relationship(
        "OrderItem", back_populates="preparations"
    )
    cook: Mapped[Cook] = relationship("Cook", back_populates="preparations")
    status: Mapped[OrderStatus] = relationship(
        "OrderStatus", back_populates="preparations"
    )


class OrderStatus(Base):
    __tablename__ = "order_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    tables: Mapped[list[Table]] = relationship("Table", back_populates="order_status")
    orders: Mapped[list[Order]] = relationship("Order", back_populates="status")
    preparations: Mapped[list["Preparation"]] = relationship(
        "Preparation", back_populates="status"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"))

    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[DECIMAL] = mapped_column(DECIMAL)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    order: Mapped[Order] = relationship("Order", back_populates="items")
    menu_item: Mapped[MenuItem] = relationship("MenuItem")
    preparations: Mapped[list[Preparation]] = relationship(
        "Preparation", back_populates="order_item"
    )


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    category: Mapped[str | None] = mapped_column(String, nullable=True)


class Cashier(Base):
    __tablename__ = "cashiers"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped[User] = relationship("User", back_populates="cashier_profile")
    payments: Mapped[list[Payment]] = relationship("Payment", back_populates="cashier")
