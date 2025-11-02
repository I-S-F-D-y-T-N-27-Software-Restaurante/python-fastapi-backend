from fastapi import APIRouter

from app.orders.dto import CreateOrderDTO
from app.orders.services import create_menu_order, get_orders_by_table_id

orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.post("/{waiter_id}/{table_id}")
def create_order(waiter_id: int, table_id: int, payload: dict):
    order_total = payload["total"]
    order_menu_item_ids = payload["menu_item_ids"]

    dto = CreateOrderDTO(
        total=order_total,
        menu_item_ids=order_menu_item_ids,
        waiter_id=waiter_id,
        table_id=table_id,
    )

    return create_menu_order(dto)


@orders_router.get("/{table_id}")
def get_orders_by_table(table_id: int):
    return get_orders_by_table_id(table_id)
