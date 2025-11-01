import logging
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError

from app.config.cnx import SessionLocal
from app.config.sql_models import MenuItem
from app.menu.dto import CreateMenuItemDTO, UpdateMenuItemDTO

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def create_menu_entry(menuItem: CreateMenuItemDTO):
    """
    Crea una entrada de menu
    """
    new_item = MenuItem(
        name=menuItem.name,
        description=menuItem.description,
        price=menuItem.price,
        available=menuItem.available,
        category=menuItem.category,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    try:
        with SessionLocal() as db:
            db.add(new_item)
            db.commit()
            db.refresh(new_item)
            logger.info(
                "Created new menu item with id %s",
                new_item.id,
            )
            return new_item

    except SQLAlchemyError as e:
        logger.error(
            "Database error while creating menu item %s: %s",
            new_item.name,
            e,
            exc_info=True,
        )
        raise


def get_all_menu_entries():
    """Busca y retorna todos las entradas de menu activas."""
    with SessionLocal() as db:
        items = db.query(MenuItem).filter(MenuItem.deleted_at.is_(None)).all()
        return items


def delete_menu_entry(item_id: int):
    """
    Marca una entrada de menu como eliminada sin borrarlo físicamente de la base de datos.
    """
    try:
        with SessionLocal() as db:
            deleted_item = db.get(MenuItem, item_id)

            if not deleted_item:
                return None

            deleted_item.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(deleted_item)

            logger.info("Soft-deleted menu item with id %s", item_id)
            return deleted_item

    except SQLAlchemyError as e:
        logger.error(
            "Database error while soft-deleting menu item %s: %s",
            item_id,
            e,
            exc_info=True,
        )
        raise


def update_menu_entry(menu_id: int, update_data: UpdateMenuItemDTO) -> MenuItem:
    try:
        with SessionLocal() as db:
            item = db.get(MenuItem, menu_id)
            if not item:
                raise ValueError(f"Menu item {menu_id} not found")

            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(item, key, value)

            db.add(item)
            db.commit()
            db.refresh(item)
            return item

    except SQLAlchemyError as e:
        logger.error(
            "Failed to update menu item: %s",
            e,
            exc_info=True,
        )
        raise
