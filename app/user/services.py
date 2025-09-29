import logging
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError

from app.config.cnx import SessionLocal
from app.config.sql_models import User
from app.user.dto import UserCreateDTO

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def get_user_by_id(user_id: int):
    """Ejecuta una busqueda para encontrar en la table usuarios un registro
    que corresponda con el id y no este borrado de manera logica."""
    with SessionLocal() as db:
        return (
            db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
        )


def get_user_by_email(email: str):
    """Busca y retorna el primer registro que coincida con el campo email."""
    with SessionLocal() as db:
        return db.query(User).filter(User.email == email).first()


def get_all_users():
    """Busca y retorna todos los usuarios activos."""
    with SessionLocal() as db:
        users = db.query(User).filter(User.deleted_at.is_(None)).all()
        return users


def create_user(user: UserCreateDTO):
    """Crea y retorna el registro de usuario si se ejecuta de manera exitosa."""
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
    """Borra de manera logica el registro de un usuario activo."""
    try:
        with SessionLocal() as db:
            user = db.get(User, user_id)

            if not user:
                return None

            user.deleted_at = datetime.now(timezone.utc)
            db.commit()

            db.refresh(user)

            logger.info("Soft-deleted user with id %s", user_id)
            return user

    except SQLAlchemyError as e:
        logger.error(
            "Database error while soft-deleting user %s: %s", user_id, e, exc_info=True
        )
        raise


def hard_delete_user(user_id: int):
    """Borra de manera PERMANENTE un registro en la base de datos."""
    try:
        with SessionLocal() as db:
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
