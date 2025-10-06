from typing import List

from fastapi import APIRouter, Depends, status

from app.config.types import Roles
from app.middlewares.security import role_required
from app.resto.dto import (
    RestoranTableCreateDTO,
    RestorantTableDTO,
    UserBaseWithRestoProfilesDTO,
)
from app.resto.services import (
    create_single_table,
    get_all_employees,
    get_employee_by_id,
    list_all_tables,
    make_user_role,
    soft_delete_table,
    tables_list_by_user,
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
