import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.config.cnx import SessionLocal
from app.config.sql_models import Cashier, Cook, User, Waiter
from app.config.types import UserProfileEnum

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def get_all_employees():
    """
    Busca y retorna todos los usuarios con perfiles de cocina activos.
    """
    with SessionLocal() as db:
        users = (
            db.query(User)
            .options(
                selectinload(User.waiter_profile),
                selectinload(User.cook_profile),
                selectinload(User.cashier_profile),
            )
            .filter(User.deleted_at.is_(None))
            .all()
        )
        return users


def get_employee_by_id(user_id: int):
    """
    Ejecuta una busqueda para encontrar en la tabla usuarios un registro
    que corresponda con el id y no este borrado de manera logica y retorna
    Usuarios con los campos de empleado completados.
    """
    with SessionLocal() as db:
        return (
            db.query(User)
            .options(
                selectinload(User.waiter_profile),
                selectinload(User.cook_profile),
                selectinload(User.cashier_profile),
            )
            .filter(User.id == user_id, User.deleted_at.is_(None))
            .first()
        )


def get_employee_by_email(email: str):
    """
    Busca y retorna el primer registro que coincida con el campo email.
    """
    with SessionLocal() as db:
        return (
            db.query(User)
            .options(
                selectinload(User.waiter_profile),
                selectinload(User.cook_profile),
                selectinload(User.cashier_profile),
            )
            .filter(User.email == email)
            .first()
        )


def make_user_role(user: User, role: UserProfileEnum):
    """
    Asigna un perfil de empleado a un usuario.
    Retorna la version actualizada con el perfil de usuario completado.
    """
    with SessionLocal() as db:
        # TODO -> implement return message instead of user
        try:
            if role == UserProfileEnum.WAITER:
                if user.waiter_profile is not None:
                    logger.info(
                        "Usuario ya tiene perfil de mesero: User id %s", user.id
                    )
                    return user

                waiter = Waiter(user=user)
                db.add(waiter)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol mesero correctamente: User id %s, Waiter id %s",
                    user.id,
                    waiter.id,
                )
                return user

            if role == UserProfileEnum.COOK:
                if user.cook_profile is not None:
                    logger.info(
                        "Usuario ya tiene perfil de cocina: User id %s", user.id
                    )
                    return user

                cook = Cook(user=user)
                db.add(cook)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol cocina correctamente: User id %s, Waiter id %s",
                    user.id,
                    cook.id,
                )
                return user

            if role == UserProfileEnum.CASHIER:
                if user.cashier_profile is not None:
                    logger.info(
                        "Usuario ya tiene perfil de cajero: User id %s", user.id
                    )
                    return user

                cashier = Cashier(user=user)
                db.add(cashier)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol cocina correctamente: User id %s, Waiter id %s",
                    user.id,
                    cashier.id,
                )
                return user

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                "Error al crear perfil actual para el usuario: User id %s: %s",
                user.id,
                e,
                exc_info=True,
            )
            raise
