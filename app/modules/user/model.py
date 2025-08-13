from datetime import datetime, timezone
from typing import Optional

from pydantic.dataclasses import dataclass
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase

from app.shared.timestamp_mixin import TimestampMixin


@dataclass(kw_only=True)
class UserSchema(TimestampMixin):
    name: str
    email: str
    password: str

    id: Optional[int] = None


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at = Column(DateTime, nullable=True)
