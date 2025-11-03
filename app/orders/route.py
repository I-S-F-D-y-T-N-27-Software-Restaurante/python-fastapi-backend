from fastapi import APIRouter, HTTPException

from app.config.types import OrderStatus
from app.orders.dto import CreateOrderDTO
from app.orders.services import (
    create_menu_order,
    get_orders_by_table_id,
    list_all_orders,
    update_order_status_for_table,
)

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


@orders_router.get("/")
def get_all_orders():
    return list_all_orders()


@orders_router.get("/{table_id}")
def get_orders_by_table(table_id: int):
    return get_orders_by_table_id(table_id)


@orders_router.post("/update/{order_id}/{new_status}")
def update_order_status(order_id: int, new_status: OrderStatus):
    try:
        order = update_order_status_for_table(order_id, new_status)
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail="Failed to update order status")
