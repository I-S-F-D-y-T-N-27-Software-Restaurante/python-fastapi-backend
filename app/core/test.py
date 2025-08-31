from datetime import datetime, timezone

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class OrderStatus(Base):
    __tablename__ = "order_statuses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    tables = relationship("Table", back_populates="order_status")
    orders = relationship("Order", back_populates="status")
    preparations = relationship("Preparation", back_populates="status")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    payments = relationship("Payment", back_populates="method")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at = Column(DateTime, nullable=True)

    role = relationship("UserRole", back_populates="users")
    waiter_profile = relationship("Waiter", back_populates="user", uselist=False)
    cook_profile = relationship("Cook", back_populates="user", uselist=False)
    cashier_profile = relationship("Cashier", back_populates="user", uselist=False)
    admin_profile = relationship("Admin", back_populates="user", uselist=False)


class Waiter(Base):
    __tablename__ = "waiters"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="waiter_profile")
    tables = relationship("Table", back_populates="waiter")
    orders = relationship("Order", back_populates="waiter")


class Cook(Base):
    __tablename__ = "cooks"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="cook_profile")
    preparations = relationship("Preparation", back_populates="cook")


class Cashier(Base):
    __tablename__ = "cashiers"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="cashier_profile")
    payments = relationship("Payment", back_populates="cashier")


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="admin_profile")
    audits = relationship("Audit", back_populates="admin")


class Table(Base):
    __tablename__ = "tables"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, nullable=False)
    waiter_id = Column(Integer, ForeignKey("waiters.id"))
    order_status_id = Column(Integer, ForeignKey("order_statuses.id"))
    occupied = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    modified_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at = Column(DateTime, nullable=True)

    waiter = relationship("Waiter", back_populates="tables")
    order_status = relationship("OrderStatus", back_populates="tables")
    orders = relationship("Order", back_populates="table")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    waiter_id = Column(Integer, ForeignKey("waiters.id"))
    status_id = Column(Integer, ForeignKey("order_statuses.id"))
    total = Column(DECIMAL)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    table = relationship("Table", back_populates="orders")
    waiter = relationship("Waiter", back_populates="orders")
    status = relationship("OrderStatus", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")
    invoice = relationship("Invoice", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL)
    notes = Column(Text)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")
    preparations = relationship("Preparation", back_populates="order_item")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(DECIMAL)
    available = Column(Boolean, default=True)
    category = Column(String)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    cashier_id = Column(Integer, ForeignKey("cashiers.id"))
    method_id = Column(Integer, ForeignKey("payment_methods.id"))
    amount = Column(DECIMAL)
    payment_time = Column(DateTime)
    notes = Column(Text)
    discounts_applied = Column(Integer)

    order = relationship("Order", back_populates="payments")
    cashier = relationship("Cashier", back_populates="payments")
    method = relationship("PaymentMethod", back_populates="payments")


class Preparation(Base):
    __tablename__ = "preparations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"))
    cook_id = Column(Integer, ForeignKey("cooks.id"))
    status_id = Column(Integer, ForeignKey("order_statuses.id"))
    start_time = Column(DateTime)
    ready_time = Column(DateTime)
    cancelled = Column(Boolean, default=False)
    cancellation_reason = Column(Text)

    order_item = relationship("OrderItem", back_populates="preparations")
    cook = relationship("Cook", back_populates="preparations")
    status = relationship("OrderStatus", back_populates="preparations")


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    issuer_id = Column(Integer)
    invoice_number = Column(String)
    issue_date = Column(DateTime)
    total_amount = Column(DECIMAL)
    details = Column(Text)

    order = relationship("Order", back_populates="invoice")


class Audit(Base):
    __tablename__ = "audits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("admins.id"))
    action = Column(String)
    description = Column(Text)
    date = Column(DateTime)
    affected_entity = Column(String)
    entity_id = Column(Integer)

    admin = relationship("Admin", back_populates="audits")
