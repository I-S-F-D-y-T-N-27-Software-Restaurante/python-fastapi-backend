import logging
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.config.cnx import SessionLocal
from app.config.sql_models import MenuItem, Order
from app.config.types import OrderStatus
from app.orders.dto import CreateOrderDTO

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def create_menu_order(order_data: CreateOrderDTO):
    """Create a new order and return it."""

    try:
        with SessionLocal() as db:
            menu_items = (
                db.query(MenuItem)
                .filter(MenuItem.id.in_(order_data.menu_item_ids))
                .all()
            )

            new_order = Order(
                waiter_id=order_data.waiter_id,
                table_id=order_data.table_id,
                total=order_data.total,
                menu_items=menu_items,
                status=OrderStatus.PENDING,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )

            db.add(new_order)
            db.commit()
            db.refresh(new_order)

            logger.info(
                "Created new order with id %s for table %s",
                new_order.id,
                new_order.table_id,
            )

            return new_order

    except SQLAlchemyError as e:
        logger.error(
            "Database error while creating order for table %s: %s",
            order_data.table_id,
            e,
            exc_info=True,
        )
        raise


def get_orders_by_table_id(table_id: int):
    with SessionLocal() as db:
        return (
            db.query(Order)
            .options(joinedload(Order.menu_items))
            .filter(Order.table_id == table_id, Order.deleted_at.is_(None))
            .all()
        )

def list_all_orders():
    with SessionLocal() as db:
        return (
            db.query(Order)
            .options(joinedload(Order.menu_items))
            .filter(Order.deleted_at.is_(None))
            .all()
        )


def update_order_status_for_table(order_id: int, new_status: str) -> Order:
    try:
        with SessionLocal() as db:
            order = db.get(Order, order_id)
            if not order:
                raise ValueError(f"Order {order_id} not found")

            order.status = OrderStatus(new_status)

            db.add(order)
            db.commit()
            db.refresh(order)
            return order

    except SQLAlchemyError as e:
        logger.error("Failed to update order status: %s", e, exc_info=True)
        raise
