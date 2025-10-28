from typing import List

from fastapi import APIRouter, Depends, status

from app.config.types import Roles
from app.middlewares.security import role_required
from app.tables.dto import RestoranTableCreateDTO, RestorantTableDTO
from app.tables.services import (
    create_single_table,
    list_all_tables,
    soft_delete_table,
    tables_list_by_user,
)

tables_router = APIRouter(prefix="/tables", tags=["Tables"])


@tables_router.get(
    "/",
    response_model=List[RestorantTableDTO],
    status_code=status.HTTP_200_OK,
    summary="Get all available tables.",
    description="This should return all tables that are not soft deleted.",
)
async def get_all_tables(
    _=Depends(role_required(Roles.WAITER)),
):
    return list_all_tables()


@tables_router.get(
    "/{user_id}",
    response_model=List[RestorantTableDTO],
    status_code=status.HTTP_200_OK,
    summary="Get table assigned to an User by ID",
    description="This should bring tables only assigned to the User in question.",
)
async def get_table_by_user_id(
    user_id: int,
    _=Depends(role_required(Roles.WAITER)),
):
    return tables_list_by_user(user_id)


@tables_router.post(
    "/",
    response_model=RestorantTableDTO,
    status_code=status.HTTP_200_OK,
    summary="Creates a restorant table.",
    description="Creates a single restorant table, for usage in tables managment.",
)
async def create_table_with_user_id(
    table: RestoranTableCreateDTO,
    _=Depends(role_required(Roles.WAITER)),
):
    return create_single_table(table)


@tables_router.delete(
    "/{table_id}",
    response_model=RestorantTableDTO,
    status_code=status.HTTP_200_OK,
    summary="Deletes a restorant table.",
    description="Soft deletes a restorant tabled by table id.",
)
async def delete_table(
    table_id: int,
    _=Depends(role_required(Roles.WAITER)),
):
    return soft_delete_table(table_id)
