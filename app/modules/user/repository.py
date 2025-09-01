from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.core.database import Session as SessionHandler
from app.core.models import User as UserModel

from .dtos import UserCreateDTO, UserUpdateDTO


class UserRepository:
    def __init__(self, session: Optional[Session] = None):
        if session is None:
            self.session = SessionHandler()
        else:
            self.session = session

    def create(self, user: UserCreateDTO) -> UserModel:
        new_user: UserModel = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        return new_user

    def get_by_id(self, user_id: int) -> UserModel | None:
        return (
            self.session.query(UserModel)
            .filter(UserModel.id == user_id, UserModel.deleted_at.is_(None))
            .first()
        )

    def get_by_email(self, email: str) -> Optional[UserModel]:
        return self.session.query(UserModel).filter(UserModel.email == email).first()

    def soft_delete(self, user_id: int) -> UserModel | None:
        user: UserModel | None = self.get_by_id(user_id)

        if not user:
            return None

        self.session.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(deleted_at=datetime.now(timezone.utc))
        )

        self.session.commit()

        return user

    def hard_delete(self, user_id: int) -> UserModel | None:
        # This gets everything, included soft deleted records
        user: UserModel | None = (
            self.session.query(UserModel).filter(UserModel.id == user_id).first()
        )

        if not user:
            return None

        self.session.delete(user)
        self.session.commit()

        return user

    def list_all(self) -> list[UserModel]:
        return (
            self.session.query(UserModel).filter(UserModel.deleted_at.is_(None)).all()
        )

    def update(self, user_id: int, user_schema: UserUpdateDTO) -> Optional[UserModel]:
        pass

    # def make_waitress(self, user_id: int) -> WaiterModel:
    #     user = self.get_by_id(user_id)
    #     if not user:
    #         raise ValueError("User not found")

    #     if user.waitress_profile:
    #         return user.waitress_profile

    #     waitress = WaiterModel(user=user)
    #     self.session.add(waitress)
    #     self.session.commit()
    #     self.session.refresh(waitress)
    #     return waitress

    # def make_cashier(self, user_id: int) -> CashierModel:
    #     user = self.get_by_id(user_id)
    #     if not user:
    #         raise ValueError("User not found")

    #     if user.cashier_profile:
    #         return user.cashier_profile

    #     cashier = CashierModel(user=user)
    #     self.session.add(cashier)
    #     self.session.commit()
    #     self.session.refresh(cashier)
    #     return cashier

    # def make_cook(self, user_id: int) -> CookModel:
    #     user = self.get_by_id(user_id)
    #     if not user:
    #         raise ValueError("User not found")

    #     if user.cook_profile:
    #         return user.cook_profile

    #     cook = CookModel(user=user)
    #     self.session.add(cook)
    #     self.session.commit()
    #     self.session.refresh(cook)
    #     return cook
