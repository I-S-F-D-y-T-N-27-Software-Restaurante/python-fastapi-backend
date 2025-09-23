from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.basemodel import Base

if TYPE_CHECKING:
    from app.resto.model import Cashier, Cook, Waiter

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    waiter_profile: Mapped["Waiter"] = relationship(
        "Waiter",
        back_populates="user",
        uselist=False,
    )
    cook_profile: Mapped["Cook"] = relationship(
        "Cook", back_populates="user", uselist=False
    )
    cashier_profile: Mapped["Cashier"] = relationship(
        "Cashier",
        back_populates="user",
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
