import logging
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.config.cnx import SessionLocal
from app.config.sql_models import Cashier, Cook, RestorantTable, User, Waiter
from app.config.types import UserProfileEnum
from app.resto.dto import RestoranTableCreateDTO

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


def make_user_role(user: User, role: UserProfileEnum):
    """
    Asigna un perfil de empleado a un usuario.
    Retorna la version actualizada con el perfil de usuario completado.
    """
    with SessionLocal() as db:
        try:
            if role == UserProfileEnum.WAITER:
                if user.waiter_profile is not None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Usuario {user.id} ya tiene perfil de mesero",
                    )

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
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Usuario {user.id} ya tiene perfil de cocina",
                    )

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
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Usuario {user.id} ya tiene perfil de cajero",
                )

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


def list_all_tables():
    """
    Busca y retorna todas las mesas disponibles.
    """
    with SessionLocal() as db:
        tables = db.query(RestorantTable).filter(User.deleted_at.is_(None)).all()
        return tables


def tables_list_by_user(user_id: int):
    """Encuentra todas las tablas asignadas a un usuario."""
    user = get_employee_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee not found.",
        )

    with SessionLocal() as db:
        return (
            db.query(RestorantTable)
            .filter(user.waiter_profile.user_id == user_id)
            .all()
        )


def find_table_by_id(table_id: int):
    with SessionLocal() as db:
        table = db.query(RestorantTable).filter(RestorantTable.id == table_id).all()

        if table is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table not found.",
            )

        return table


def create_single_table(table: RestoranTableCreateDTO):
    new_table = RestorantTable(
        number=table.number,
        waiter_id=table.waiter_id,
        order_status_id=table.order_status_id,
        occupied=table.occupied,
        notes=table.notes,
    )
    try:
        with SessionLocal() as db:
            db.add(new_table)
            db.commit()
            db.refresh(new_table)
            logger.info(
                "Created new table with id %s and waiter.id %s",
                new_table.id,
                new_table.waiter.id,
            )
            return new_table

    except SQLAlchemyError as e:
        logger.error(
            "Database error while creating table %s: %s",
            RestorantTable.id,
            e,
            exc_info=True,
        )
        raise


def soft_delete_table(table_id: int):
    """Borra de manera logica la mesa con el id dado."""
    try:
        with SessionLocal() as db:
            table = db.get(RestorantTable, table_id)
            if not table:
                raise HTTPException(status_code=404, detail="Table not found")

            table.deleted_at = datetime.now(timezone.utc)
            db.commit()

            db.refresh(table)

            logger.info("Soft-deleted user with id %s", table.id)
            return table

    except SQLAlchemyError as e:
        logger.error(
            "Database error while soft-deleting table %s: %s",
            table_id,
            e,
            exc_info=True,
        )
        raise
