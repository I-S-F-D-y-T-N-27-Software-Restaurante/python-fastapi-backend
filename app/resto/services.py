import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.config.cnx import SessionLocal
from app.config.sql_models import Cashier, Cook, User, Waiter
from app.config.types import Roles

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
        user = (
            db.query(User)
            .options(
                selectinload(User.waiter_profile),
                selectinload(User.cook_profile),
                selectinload(User.cashier_profile),
            )
            .filter(User.id == user_id, User.deleted_at.is_(None))
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee not found.",
            )

        return user


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


def make_user_role(user: User, role: Roles):
    """
    Asigna perfiles de empleado a un usuario.
    Puede asignar múltiples roles en un solo llamado.
    Retorna la versión actualizada del usuario con los perfiles cargados.
    """
    with SessionLocal() as db:
        try:
            # Merge detached user into current session
            user = db.merge(user)

            if role == Roles.WAITER:
                if user.waiter_profile:
                    raise ValueError(f"Usuario {user.id} ya tiene perfil de mesero")

                waiter = Waiter(user=user)
                db.add(waiter)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol mesero correctamente: User id %s, Waiter id %s",
                    user.id,
                    waiter.id,
                )

            elif role == Roles.COOK:
                if user.cook_profile:
                    raise ValueError(f"Usuario {user.id} ya tiene perfil de cocina")

                cook = Cook(user=user)
                db.add(cook)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol cocina correctamente: User id %s, Cook id %s",
                    user.id,
                    cook.id,
                )

            elif role == Roles.CASHIER:
                if user.cashier_profile:
                    raise ValueError(f"Usuario {user.id} ya tiene perfil de cajero")

                cashier = Cashier(user=user)
                db.add(cashier)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol cajero correctamente: User id %s, Cashier id %s",
                    user.id,
                    cashier.id,
                )

            else:
                raise ValueError(f"Rol no reconocido: {role}")

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

