from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


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

    waitress_profile = relationship(
        "WaitressModel",
        back_populates="user",
        uselist=False,
    )


class WaitressModel(Base):
    __tablename__ = "waitress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("UserModel", back_populates="waitress_profile")


# class CookModel(Base):
#     __tablename__ = "cook"

#     id = Column(Integer, primary_key=True, autoincrement=True)


# class CashierModel(Base):
#     __tablename__ = "cashier"

#     id = Column(Integer, primary_key=True, autoincrement=True)
