from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.config.cnx import get_db
from app.config.types import Roles
from app.middlewares.security import get_current_user_token, role_required
from app.tables.dto import TableCreateDTO, TableUpdateDTO, TableResponseDTO
from app.tables.services import (
    get_tables,
    get_table_by_id,
    get_tables_by_waiter,
    create_table,
    update_table,
    soft_delete_table
)

tables_router = APIRouter(prefix="/tables", tags=["Tables"])



@tables_router.get("/", response_model=List[TableResponseDTO])
def list_tables(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_token)  # todos los usuarios autenticados pueden listar
):
    """Lista todas las mesas activas."""
    return get_tables(db)


@tables_router.get("/by_waiter/{waiter_id}", response_model=List[TableResponseDTO])
def list_tables_by_waiter(
    waiter_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_token)  # todos los usuarios autenticados
):
    """Obtiene las mesas asignadas a un mozo."""
    return get_tables_by_waiter(db, waiter_id)


@tables_router.get("/{table_id}", response_model=TableResponseDTO)
def get_table(
    table_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_token)  # todos los usuarios autenticados
):
    """Obtiene una mesa específica por ID."""
    return get_table_by_id(db, table_id)


@tables_router.post(
    "/", response_model=TableResponseDTO, status_code=201
)
def create_new_table(
    data: TableCreateDTO,
    db: Session = Depends(get_db),
    token=Depends(role_required(Roles.WAITER))  # WAITER o ADMIN
):
    """Crea una nueva mesa."""
    return create_table(db, data)


@tables_router.put("/{table_id}", response_model=TableResponseDTO)
def modify_table(
    table_id: int,
    data: TableUpdateDTO,
    db: Session = Depends(get_db),
    token=Depends(role_required(Roles.WAITER))  # WAITER o ADMIN
):
    """Actualiza una mesa existente."""
    return update_table(db, table_id, data)


@tables_router.delete("/{table_id}")
def remove_table(
    table_id: int,
    db: Session = Depends(get_db),
    token=Depends(role_required(Roles.WAITER))  # WAITER o ADMIN
):
    """Borrado lógico de una mesa."""
    return soft_delete_table(db, table_id)