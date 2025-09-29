from typing import List

from fastapi import APIRouter, status

from app.config.types import UserProfileEnum
from app.resto.dto import (
    RestoranTableCreateDTO,
    RestorantTableDTO,
    UpdateRestorantTableDTO,
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
    update_restorant_table,
)

resto_router = APIRouter(prefix="/resto")


@resto_router.get(
    "/",
    response_model=List[UserBaseWithRestoProfilesDTO],
    status_code=status.HTTP_200_OK,
)
async def list_users():
    return get_all_employees()


@resto_router.post(
    "/roles/{user_id}/{role}",
    response_model=UserBaseWithRestoProfilesDTO,
    status_code=status.HTTP_200_OK,
)
async def make_user_profile(user_id: str, role: UserProfileEnum):
    user = get_employee_by_id(user_id)
    return make_user_role(user, role)


@resto_router.get(
    "/roles/{user_id}",
    response_model=UserBaseWithRestoProfilesDTO,
    status_code=status.HTTP_200_OK,
)
async def get_single_user_with_profile(user_id: int):
    return get_employee_by_id(user_id)


@resto_router.get(
    "/tables",
    response_model=List[RestorantTableDTO],
    status_code=status.HTTP_200_OK,
)
async def get_all_tables():
    return list_all_tables()


@resto_router.get(
    "/tables/{user_id}",
    response_model=List[RestorantTableDTO],
    status_code=status.HTTP_200_OK,
)
async def get_table_by_user_id(user_id: int):
    return tables_list_by_user(user_id)


@resto_router.post(
    "/tables",
    response_model=RestorantTableDTO,
    status_code=status.HTTP_200_OK,
)
async def create_table_with_user_id(table: RestoranTableCreateDTO):
    return create_single_table(table)


@resto_router.post(
    "/tables",
    response_model=RestorantTableDTO,
    status_code=status.HTTP_200_OK,
)
async def delete_table(table_id: int):
    return soft_delete_table(table_id)

@resto_router.patch(
    "/tables/{table_id}",
    response_model=UpdateRestorantTableDTO,
    status_code=status.HTTP_200_OK,
)
async def modify_table_info(table_id: int, table: UpdateRestorantTableDTO):
    return update_restorant_table(table_id, table)
