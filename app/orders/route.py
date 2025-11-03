from fastapi import APIRouter, HTTPException, status

from app.config.types import OrderStatus
from app.orders.dto import CreateOrderDTO
from app.orders.services import (
    create_menu_order,
    get_orders_by_table_id,
    list_all_orders,
    update_order_status_for_table,
)

orders_router = APIRouter(prefix="/orders", tags=["Orders"])


@orders_router.post(
    "/{waiter_id}/{table_id}",
    summary="Create a new order",
    description="Create a new order for a specific waiter and table. Requires a payload containing 'total' and 'menu_item_ids'.",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "OK"}},
)
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


@orders_router.get(
    "/",
    summary="List all orders",
    description="Retrieve a list of all orders in the system.",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "OK"}},
)
def get_all_orders():
    return list_all_orders()


@orders_router.get(
    "/{table_id}",
    summary="Get orders by table",
    description="Retrieve all orders associated with a specific table ID.",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "OK"}},
)
def get_orders_by_table(table_id: int):
    return get_orders_by_table_id(table_id)


@orders_router.post(
    "/update/{order_id}/{new_status}",
    summary="Update order status",
    description="Update the status of a specific order by its ID. Provide the new status in the path.",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "OK"}},
)
def update_order_status(order_id: int, new_status: OrderStatus):
    try:
        order = update_order_status_for_table(order_id, new_status)
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update order status")
