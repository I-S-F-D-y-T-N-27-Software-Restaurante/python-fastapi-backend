from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.basemodel import Base
from app.config.types import OrderStatus, RestaurantTableStatus


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    waiter_profile: Mapped["Waiter"] = relationship(
        "Waiter",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    cook_profile: Mapped["Cook"] = relationship(
        "Cook",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    cashier_profile: Mapped["Cashier"] = relationship(
        "Cashier",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Waiter(Base):
    __tablename__ = "waiters"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, unique=True
    )

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="waiter_profile")

    tables: Mapped[list["RestorantTable"]] = relationship(
        "RestorantTable", back_populates="waiter"
    )
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="waiter")


class Cashier(Base):
    __tablename__ = "cashiers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="cashier_profile")


class Cook(Base):
    __tablename__ = "cooks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship("User", back_populates="cook_profile")


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class RestorantTable(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    waiter_id: Mapped[int] = mapped_column(ForeignKey("waiters.id"))

    status: Mapped[RestaurantTableStatus] = mapped_column(
        SqlEnum(RestaurantTableStatus, name="restaurant_table_status_enum"),
        nullable=False,
        default=RestaurantTableStatus.AVAILABLE,
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    waiter: Mapped["Waiter"] = relationship("Waiter", back_populates="tables")

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="table")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


# Association table between Order and MenuItem
order_menuitem_association = Table(
    "order_menuitem_association",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("menu_item_id", ForeignKey("menu_items.id"), primary_key=True),
)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))

    waiter_id: Mapped[int] = mapped_column(ForeignKey("waiters.id"))

    total: Mapped[DECIMAL] = mapped_column(DECIMAL)

    table: Mapped["RestorantTable"] = relationship(
        "RestorantTable", back_populates="orders"
    )

    waiter: Mapped["Waiter"] = relationship("Waiter", back_populates="orders")

    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus, name="order_status_enum"),
        nullable=False,
        default=OrderStatus.UNASSIGNED,
    )

    menu_items: Mapped[list["MenuItem"]] = relationship(
        "MenuItem",
        secondary=order_menuitem_association,
        back_populates="orders",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    category: Mapped[str | None] = mapped_column(String, nullable=True)

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        secondary=order_menuitem_association,
        back_populates="menu_items",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
