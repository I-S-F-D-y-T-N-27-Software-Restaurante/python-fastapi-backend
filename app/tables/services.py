import logging
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.config.cnx import SessionLocal
from app.config.sql_models import RestorantTable
from app.resto.services import get_employee_by_id
from app.tables.dto import RestoranTableCreateDTO

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def list_all_tables():
    """
    Busca y retorna todas las mesas disponibles.
    """
    with SessionLocal() as db:
        tables = (
            db.query(RestorantTable).filter(RestorantTable.deleted_at.is_(None)).all()
        )
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
        waiter_id=table.waiter_id, notes=table.notes, status=table.status
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

            logger.info("Soft-deleted table with id %s", table.id)
            return table

    except SQLAlchemyError as e:
        logger.error(
            "Database error while soft-deleting table %s: %s",
            table_id,
            e,
            exc_info=True,
        )
        raise
