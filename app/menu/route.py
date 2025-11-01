from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.config.types import Roles
from app.menu.dto import CreateMenuItemDTO, MenuItemDTO, UpdateMenuItemDTO
from app.menu.services import (
    create_menu_entry,
    delete_menu_entry,
    get_all_menu_entries,
    update_menu_entry,
)
from app.middlewares.security import role_required

menu_router = APIRouter(prefix="/menu", tags=["Menu"])


@menu_router.post(
    "/",
    response_model=CreateMenuItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Creates a new menu entry",
    description="Creates a entry with description, price and category",
)
async def create_menu_item(
    menu_item: CreateMenuItemDTO,
    _=Depends(role_required(Roles.COOK)),
):
    return create_menu_entry(menu_item)


@menu_router.get(
    "/",
    response_model=List[MenuItemDTO],
    status_code=status.HTTP_200_OK,
    summary="Get all menu items",
    description="Get all menu items that are not soft deleted",
)
async def list_menu_items(
    _=Depends(role_required(Roles.COOK)),
):
    return get_all_menu_entries()


@menu_router.delete(
    "/{menu_item_id}",
    response_model=MenuItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Delete menu item",
    description="Soft delete menu item with a given ID",
)
async def delete_menu_item(
    menu_item_id: int,
    _=Depends(role_required(Roles.COOK)),
):
    return delete_menu_entry(menu_item_id)


@menu_router.put(
    "/{menu_id}",
    response_model=MenuItemDTO,
    status_code=status.HTTP_200_OK,
    summary="Update menu item",
    description="Update fields of a menu item by ID",
)
async def update_menu_item(
    menu_id: int,
    menu_item: UpdateMenuItemDTO,
    _=Depends(role_required(Roles.COOK)),
):
    try:
        updated_item = update_menu_entry(menu_id, menu_item)
        return updated_item
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
