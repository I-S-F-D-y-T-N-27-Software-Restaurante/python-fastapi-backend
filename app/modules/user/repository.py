from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.core.models import CashierModel, CookModel, UserModel, WaitressModel
from app.modules.user.entities import User, UserEntity


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> UserModel:
        user = UserModel(
            name=user.name,
            email=user.email,
            password=user.password,
            created_at=user.created_at or datetime.now(timezone.utc),
            updated_at=user.updated_at or datetime.now(timezone.utc),
            deleted_at=user.deleted_at,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.session.query(UserModel).filter(UserModel.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[UserModel]:
        return self.session.query(UserModel).filter(UserModel.email == email).first()

    def update(self, user_id: int, user_schema: UserEntity) -> Optional[UserModel]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        user.name = user_schema.name
        user.email = user_schema.email
        user.password = user_schema.password
        user.updated_at = datetime.now(timezone.utc)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        user.deleted_at = datetime.now(timezone.utc)
        self.session.commit()
        return True

    def list_all(self) -> list[UserModel]:
        return self.session.query(UserModel).filter(UserModel.deleted_at is None).all()

    def make_waitress(self, user_id: int) -> WaitressModel:
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if user.waitress_profile:
            return user.waitress_profile

        waitress = WaitressModel(user=user)
        self.session.add(waitress)
        self.session.commit()
        self.session.refresh(waitress)
        return waitress

    def make_cashier(self, user_id: int) -> CashierModel:
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if user.cashier_profile:
            return user.cashier_profile

        cashier = CashierModel(user=user)
        self.session.add(cashier)
        self.session.commit()
        self.session.refresh(cashier)
        return cashier

    def make_cook(self, user_id: int) -> CookModel:
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if user.cook_profile:
            return user.cook_profile

        cook = CookModel(user=user)
        self.session.add(cook)
        self.session.commit()
        self.session.refresh(cook)
        return cook
