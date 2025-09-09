from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.basemodel import Base
from app.config.types import TimestampMixin

if TYPE_CHECKING:
    from app.user.model import User


class Admin(Base, TimestampMixin):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    user: Mapped[User] = relationship(back_populates="admin_profile")
    audits: Mapped[list[Audit]] = relationship(back_populates="admin")


class Audit(Base, TimestampMixin):
    __tablename__ = "audits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id"))
    action: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date: Mapped[DateTime] = mapped_column(DateTime)
    affected_entity: Mapped[str | None] = mapped_column(String, nullable=True)
    entity_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    admin: Mapped[Admin] = relationship(back_populates="audits")
