from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.config.sql_models import RestorantTable
from app.tables.dto import TableCreateDTO, TableUpdateDTO


def get_tables(db: Session):
    """Obtiene todas las mesas activas (no eliminadas)."""
    return db.query(RestorantTable).filter(RestorantTable.deleted_at == None).all()


def get_table_by_id(db: Session, table_id: int):
    """Obtiene una mesa específica por ID."""
    table = db.query(RestorantTable).filter(
        RestorantTable.id == table_id,
        RestorantTable.deleted_at == None
    ).first()
    if not table:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    return table


def get_tables_by_waiter(db: Session, waiter_id: int):
    """Obtiene todas las mesas asignadas a un mozo específico."""
    tables = db.query(RestorantTable).filter(
        RestorantTable.waiter_id == waiter_id,
        RestorantTable.deleted_at == None
    ).all()
    return tables


def create_table(db: Session, data: TableCreateDTO):
    """Crea una nueva mesa verificando que no exista otra con el mismo número."""
    existing = db.query(RestorantTable).filter(
        RestorantTable.number == data.number,
        RestorantTable.deleted_at == None
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una mesa con ese número")

    new_table = RestorantTable(**data.dict())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return new_table


def update_table(db: Session, table_id: int, data: TableUpdateDTO):
    """Actualiza los datos de una mesa existente."""
    table = get_table_by_id(db, table_id)
    for key, value in data.dict(exclude_unset=True).items():
        setattr(table, key, value)
    db.commit()
    db.refresh(table)
    return table


def soft_delete_table(db: Session, table_id: int):
    """Realiza un borrado lógico de la mesa."""
    table = get_table_by_id(db, table_id)
    table.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(table)
    return {"message": f"Mesa {table_id} eliminada correctamente"}