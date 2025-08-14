from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.core.models import UserModel
from app.modules.user.entity import UserEntity


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_schema: UserEntity) -> UserModel:
        user = UserModel(
            name=user_schema.name,
            email=user_schema.email,
            password=user_schema.password,
            created_at=user_schema.created_at or datetime.now(timezone.utc),
            updated_at=user_schema.updated_at or datetime.now(timezone.utc),
            deleted_at=user_schema.deleted_at,
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
