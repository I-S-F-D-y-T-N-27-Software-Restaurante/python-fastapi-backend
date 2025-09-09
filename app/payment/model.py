from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.basemodel import Base
from app.config.types import TimestampMixin

if TYPE_CHECKING:
    from app.resto.model import Cashier, Order


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    cashier_id: Mapped[int] = mapped_column(ForeignKey("cashiers.id"))
    method_id: Mapped[int] = mapped_column(ForeignKey("payment_methods.id"))

    amount: Mapped[DECIMAL] = mapped_column(DECIMAL)
    payment_time: Mapped[datetime] = mapped_column(DateTime)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    discounts_applied: Mapped[int | None] = mapped_column(Integer, nullable=True)

    order: Mapped[Order] = relationship("Order", back_populates="payments")
    cashier: Mapped[Cashier] = relationship("Cashier", back_populates="payments")
    method: Mapped[PaymentMethod] = relationship(
        "PaymentMethod", back_populates="payments"
    )


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    payments: Mapped[list[Payment]] = relationship("Payment", back_populates="method")


class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    issuer_id: Mapped[int] = mapped_column()
    invoice_number: Mapped[str] = mapped_column(String)
    issue_date: Mapped[datetime] = mapped_column(DateTime)
    total_amount: Mapped[DECIMAL] = mapped_column(DECIMAL)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)

    order: Mapped[Order] = relationship("Order", back_populates="invoice")
