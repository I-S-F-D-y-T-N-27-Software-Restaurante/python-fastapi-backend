import logging
from datetime import datetime, timezone

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from app.config.cnx import SessionLocal
from app.user.dto import UserCreateDTO
from app.user.model import User

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def get_user_by_id(user_id: int):
    with SessionLocal() as db:
        return (
            db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
        )


def get_user_by_email(email: str):
    with SessionLocal() as db:
        return db.query(User).filter(User.email == email).first()


def get_all_users():
    with SessionLocal() as db:
        users = db.query(User).filter(User.deleted_at.is_(None)).all()
        logger.info(f"{len(users)} users were retrieved")
        logger.info(f"first entry is {users[0]}")
        return users


def create_user(user: UserCreateDTO):
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    try:
        with SessionLocal() as db:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info(
                "Created new user with id %s and email %s", new_user.id, new_user.email
            )
            return new_user

    except SQLAlchemyError as e:
        logger.error(
            "Database error while creating user %s: %s",
            new_user.email,
            e,
            exc_info=True,
        )
        raise


def soft_delete_user(user_id: int):
    user = get_user_by_id(user_id)

    if not user:
        return None

    try:
        with SessionLocal() as db:
            db.execute(
                update(User)
                .where(User.id == user_id)
                .values(deleted_at=datetime.now(timezone.utc))
            )
            db.commit()
            logger.info("Soft-deleted user with id %s", user_id)
            return user

    except SQLAlchemyError as e:
        logger.error(
            "Database error while soft-deleting user %s: %s", user_id, e, exc_info=True
        )
        raise


def hard_delete_user(user_id: int):
    try:
        with SessionLocal() as db:
            # Fetch user, including soft-deleted ones
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None

            db.delete(user)
            db.commit()
            logger.info("Hard-deleted user with id %s", user_id)
            return user

    except SQLAlchemyError as e:
        logger.error(
            "Database error while hard-deleting user %s: %s", user_id, e, exc_info=True
        )
        raise
