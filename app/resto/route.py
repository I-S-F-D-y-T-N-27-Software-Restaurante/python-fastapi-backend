from typing import List
from fastapi import APIRouter, Depends, status

from app.config.types import Roles
from app.middlewares.security import role_required
from app.resto.dto import (
    UserBaseWithRestoProfilesDTO,
    OrderCreateDTO,
    OrderDTO,
)
from app.resto.services import (
    get_all_employees,
    get_employee_by_id,
    make_user_role,
    create_order,
    get_order_by_id,
    list_all_orders,
    update_order_status,
    soft_delete_order,
)

# ✅ Definimos correctamente el router
resto_router = APIRouter(prefix="/resto", tags=["Resto"])

# ===========================
#        EMPLEADOS
# ===========================

@resto_router.get("/", response_model=List[UserBaseWithRestoProfilesDTO])
async def list_users(_=Depends(role_required(Roles.ADMIN))):
    """Obtiene todos los empleados del restaurante."""
    return get_all_employees()


@resto_router.post("/roles/{user_id}/{role}", response_model=UserBaseWithRestoProfilesDTO)
async def make_user_profile(user_id: int, role: Roles, _=Depends(role_required(Roles.ADMIN))):
    """Asigna un rol (waiter, cook o cashier) a un usuario."""
    user = get_employee_by_id(user_id)
    return make_user_role(user, role)


@resto_router.get("/roles/{user_id}", response_model=UserBaseWithRestoProfilesDTO)
async def get_single_user_with_profile(user_id: int, _=Depends(role_required(Roles.ADMIN))):
    """Obtiene un empleado con sus perfiles asociados."""
    return get_employee_by_id(user_id)

# ===========================
#         PEDIDOS
# ===========================

@resto_router.post("/orders", response_model=OrderDTO, status_code=status.HTTP_201_CREATED)
async def create_new_order(order: OrderCreateDTO, _=Depends(role_required(Roles.WAITER))):
    """Crea un nuevo pedido."""
    return create_order(order)


@resto_router.get("/orders", response_model=List[OrderDTO])
async def get_all_orders(_=Depends(role_required(Roles.WAITER))):
    """Lista todos los pedidos activos."""
    return list_all_orders()


@resto_router.get("/orders/{order_id}", response_model=OrderDTO)
async def get_single_order(order_id: int, _=Depends(role_required(Roles.WAITER))):
    """Obtiene un pedido por ID."""
    return get_order_by_id(order_id)


@resto_router.patch("/orders/{order_id}/status/{status_id}", response_model=OrderDTO)
async def update_order_state(order_id: int, status_id: int, _=Depends(role_required(Roles.WAITER))):
    """Actualiza el estado de un pedido."""
    return update_order_status(order_id, status_id)


@resto_router.delete("/orders/{order_id}", response_model=OrderDTO)
async def delete_order_by_id(order_id: int, _=Depends(role_required(Roles.WAITER))):
    """Elimina lógicamente un pedido."""
    return soft_delete_order(order_id)