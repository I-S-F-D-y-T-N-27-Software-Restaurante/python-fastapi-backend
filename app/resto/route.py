from typing import List

from fastapi import APIRouter, Depends, status

from app.config.types import Roles
from app.middlewares.security import role_required
from app.resto.dto import (
    RestoranTableCreateDTO,
    RestorantTableDTO,
    UserBaseWithRestoProfilesDTO,
    OrderCreateDTO,
    OrderDTO,
)
from app.resto.services import (
    create_single_table,
    get_all_employees,
    get_employee_by_id,
    list_all_tables,
    make_user_role,
    soft_delete_table,
    tables_list_by_user,
    create_order,
    get_order_by_id,
    list_all_orders,
    update_order_status,
    soft_delete_order,
)

resto_router = APIRouter(prefix="/resto")


@resto_router.get(
    "/",
    response_model=List[UserBaseWithRestoProfilesDTO],
    status_code=status.HTTP_200_OK,
)
async def list_users(
    _=Depends(role_required(Roles.ADMIN)),
):
    return get_all_employees()


@resto_router.post(
    "/roles/{user_id}/{role}",
    response_model=UserBaseWithRestoProfilesDTO,
    status_code=status.HTTP_200_OK,
)
async def make_user_profile(
    user_id: int,
    role: Roles,
    _=Depends(role_required(Roles.ADMIN)),
):
    user = get_employee_by_id(user_id)
    return make_user_role(user, role)


@resto_router.get(
    "/roles/{user_id}",
    response_model=UserBaseWithRestoProfilesDTO,
    status_code=status.HTTP_200_OK,
)
async def get_single_user_with_profile(
    user_id: int,
    _=Depends(role_required(Roles.ADMIN)),
):
    return get_employee_by_id(user_id)


@resto_router.get(
    "/tables",
    response_model=List[RestorantTableDTO],
    status_code=status.HTTP_200_OK,
)
async def get_all_tables(
    _=Depends(role_required(Roles.WAITER)),
):
    return list_all_tables()


@resto_router.get(
    "/tables/{user_id}",
    response_model=List[RestorantTableDTO],
    status_code=status.HTTP_200_OK,
)
async def get_table_by_user_id(
    user_id: int,
    _=Depends(role_required(Roles.WAITER)),
):
    return tables_list_by_user(user_id)


@resto_router.post(
    "/tables",
    response_model=RestorantTableDTO,
    status_code=status.HTTP_200_OK,
)
async def create_table_with_user_id(
    table: RestoranTableCreateDTO,
    _=Depends(role_required(Roles.WAITER)),
):
    return create_single_table(table)


@resto_router.post(
    "/tables",
    response_model=RestorantTableDTO,
    status_code=status.HTTP_200_OK,
)
async def delete_table(
    table_id: int,
    _=Depends(role_required(Roles.WAITER)),
):
    return soft_delete_table(table_id)

# ==============================
#           ORDERS
# ==============================

@resto_router.post(
    "/orders",
    response_model=OrderDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_order(
    order: OrderCreateDTO,
    _=Depends(role_required(Roles.WAITER)),
):
    """
    Crea un nuevo pedido junto con sus ítems.
    Solo accesible por mozos.
    """
    return create_order(order)


@resto_router.get(
    "/orders",
    response_model=List[OrderDTO],
    status_code=status.HTTP_200_OK,
)
async def get_all_orders(
    _=Depends(role_required(Roles.WAITER)),
):
    """
    Lista todos los pedidos activos con sus ítems.
    """
    return list_all_orders()


@resto_router.get(
    "/orders/{order_id}",
    response_model=OrderDTO,
    status_code=status.HTTP_200_OK,
)
async def get_single_order(
    order_id: int,
    _=Depends(role_required(Roles.WAITER)),
):
    """
    Obtiene un pedido específico con sus ítems.
    """
    return get_order_by_id(order_id)


@resto_router.patch(
    "/orders/{order_id}/status/{status_id}",
    response_model=OrderDTO,
    status_code=status.HTTP_200_OK,
)
async def update_order_state(
    order_id: int,
    status_id: int,
    _=Depends(role_required(Roles.WAITER)),
):
    """
    Cambia el estado de un pedido existente.
    """
    return update_order_status(order_id, status_id)


@resto_router.delete(
    "/orders/{order_id}",
    response_model=OrderDTO,
    status_code=status.HTTP_200_OK,
)
async def delete_order_by_id(
    order_id: int,
    _=Depends(role_required(Roles.WAITER)),
):
    """
    Realiza un borrado lógico del pedido.
    """
    return soft_delete_order(order_id)
