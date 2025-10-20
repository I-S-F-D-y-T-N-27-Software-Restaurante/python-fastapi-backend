import logging
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.config.cnx import SessionLocal
from app.config.sql_models import Cashier, Cook, RestorantTable, User, Waiter , Order, OrderItem, OrderStatus
from app.config.types import Roles
from app.resto.dto import RestoranTableCreateDTO , OrderCreateDTO

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def get_all_employees():
    """
    Busca y retorna todos los usuarios con perfiles de cocina activos.
    """
    with SessionLocal() as db:
        users = (
            db.query(User)
            .options(
                selectinload(User.waiter_profile),
                selectinload(User.cook_profile),
                selectinload(User.cashier_profile),
            )
            .filter(User.deleted_at.is_(None))
            .all()
        )
        return users


def get_employee_by_id(user_id: int):
    """
    Ejecuta una busqueda para encontrar en la tabla usuarios un registro
    que corresponda con el id y no este borrado de manera logica y retorna
    Usuarios con los campos de empleado completados.
    """
    with SessionLocal() as db:
        user = (
            db.query(User)
            .options(
                selectinload(User.waiter_profile),
                selectinload(User.cook_profile),
                selectinload(User.cashier_profile),
            )
            .filter(User.id == user_id, User.deleted_at.is_(None))
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee not found.",
            )

        return user


def get_employee_by_email(email: str):
    """
    Busca y retorna el primer registro que coincida con el campo email.
    """
    with SessionLocal() as db:
        return (
            db.query(User)
            .options(
                selectinload(User.waiter_profile),
                selectinload(User.cook_profile),
                selectinload(User.cashier_profile),
            )
            .filter(User.email == email)
            .first()
        )


def make_user_role(user: User, role: Roles):
    """
    Asigna un perfil de empleado a un usuario.
    Retorna la version actualizada con el perfil de usuario completado.
    """
    with SessionLocal() as db:
        try:
            if role == Roles.WAITER:
                if user.waiter_profile is not None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Usuario {user.id} ya tiene perfil de mesero",
                    )

                waiter = Waiter(user=user)
                db.add(waiter)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol mesero correctamente: User id %s, Waiter id %s",
                    user.id,
                    waiter.id,
                )
                return user

            if role == Roles.COOK:
                if user.cook_profile is not None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Usuario {user.id} ya tiene perfil de cocina",
                    )

                cook = Cook(user=user)
                db.add(cook)
                db.commit()
                db.refresh(user)
                logger.info(
                    "Usuario convertido a rol cocina correctamente: User id %s, Waiter id %s",
                    user.id,
                    cook.id,
                )
                return user

            if role == Roles.CASHIER:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Usuario {user.id} ya tiene perfil de cajero",
                )

            cashier = Cashier(user=user)
            db.add(cashier)
            db.commit()
            db.refresh(user)
            logger.info(
                "Usuario convertido a rol cocina correctamente: User id %s, Waiter id %s",
                user.id,
                cashier.id,
            )
            return user

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                "Error al crear perfil actual para el usuario: User id %s: %s",
                user.id,
                e,
                exc_info=True,
            )
            raise


def list_all_tables():
    """
    Busca y retorna todas las mesas disponibles.
    """
    with SessionLocal() as db:
        tables = db.query(RestorantTable).filter(User.deleted_at.is_(None)).all()
        return tables


def tables_list_by_user(user_id: int):
    """Encuentra todas las tablas asignadas a un usuario."""
    user = get_employee_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee not found.",
        )

    with SessionLocal() as db:
        return (
            db.query(RestorantTable)
            .filter(user.waiter_profile.user_id == user_id)
            .all()
        )


def find_table_by_id(table_id: int):
    with SessionLocal() as db:
        table = db.query(RestorantTable).filter(RestorantTable.id == table_id).all()

        if table is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table not found.",
            )

        return table


def create_single_table(table: RestoranTableCreateDTO):
    new_table = RestorantTable(
        number=table.number,
        waiter_id=table.waiter_id,
        order_status_id=table.order_status_id,
        occupied=table.occupied,
        notes=table.notes,
    )
    try:
        with SessionLocal() as db:
            db.add(new_table)
            db.commit()
            db.refresh(new_table)
            logger.info(
                "Created new table with id %s and waiter.id %s",
                new_table.id,
                new_table.waiter.id,
            )
            return new_table

    except SQLAlchemyError as e:
        logger.error(
            "Database error while creating table %s: %s",
            RestorantTable.id,
            e,
            exc_info=True,
        )
        raise


def soft_delete_table(table_id: int):
    """Borra de manera logica la mesa con el id dado."""
    try:
        with SessionLocal() as db:
            table = db.get(RestorantTable, table_id)
            if not table:
                raise HTTPException(status_code=404, detail="Table not found")

            table.deleted_at = datetime.now(timezone.utc)
            db.commit()

            db.refresh(table)

            logger.info("Soft-deleted user with id %s", table.id)
            return table

    except SQLAlchemyError as e:
        logger.error(
            "Database error while soft-deleting table %s: %s",
            table_id,
            e,
            exc_info=True,
        )
        raise

def create_order(order_data: OrderCreateDTO):
    """
    Crea un nuevo pedido junto con sus items.
    """
    try:
        with SessionLocal() as db:
            # Validar mesa y mozo existentes
            table = db.get(RestorantTable, order_data.table_id)
            waiter = db.get(Waiter, order_data.waiter_id)
            status = db.get(OrderStatus, order_data.status_id)

            if not table or table.deleted_at:
                raise HTTPException(status_code=400, detail="Table not found or deleted.")
            if not waiter or waiter.deleted_at:
                raise HTTPException(status_code=400, detail="Waiter not found or deleted.")
            if not status:
                raise HTTPException(status_code=400, detail="Invalid order status.")

            # Crear el pedido principal
            new_order = Order(
                table_id=order_data.table_id,
                waiter_id=order_data.waiter_id,
                status_id=order_data.status_id,
                total=Decimal(order_data.total),
                notes=order_data.notes,
            )
            db.add(new_order)
            db.flush()  # para obtener el ID antes de crear los ítems

            # Crear los items asociados
            for item in order_data.items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    menu_item_id=item.menu_item_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    notes=item.notes,
                )
                db.add(order_item)

            db.commit()
            db.refresh(new_order)

            logger.info("Order created successfully with id %s", new_order.id)
            return new_order

    except SQLAlchemyError as e:
        logger.error("Error creating order: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Database error while creating order.")

def get_order_by_id(order_id: int):
    """
    Retorna un pedido por ID, incluyendo sus ítems.
    """
    with SessionLocal() as db:
        order = (
            db.query(Order)
            .options(selectinload(Order.items))
            .filter(Order.id == order_id, Order.deleted_at.is_(None))
            .first()
        )

        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")

        return order

def list_all_orders():
    """
    Retorna todos los pedidos activos con sus ítems.
    """
    with SessionLocal() as db:
        orders = (
            db.query(Order)
            .options(selectinload(Order.items))
            .filter(Order.deleted_at.is_(None))
            .all()
        )
        return orders

def update_order_status(order_id: int, new_status_id: int):
    """
    Cambia el estado de un pedido.
    """
    try:
        with SessionLocal() as db:
            order = db.get(Order, order_id)
            if not order or order.deleted_at:
                raise HTTPException(status_code=404, detail="Order not found.")

            status = db.get(OrderStatus, new_status_id)
            if not status:
                raise HTTPException(status_code=400, detail="Invalid status ID.")

            order.status_id = new_status_id
            order.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(order)

            logger.info(
                "Order %s updated to status %s", order_id, new_status_id
            )
            return order

    except SQLAlchemyError as e:
        logger.error("Error updating order status: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Database error while updating order.")

def soft_delete_order(order_id: int):
    """
    Marca un pedido como eliminado (soft delete).
    """
    try:
        with SessionLocal() as db:
            order = db.get(Order, order_id)
            if not order or order.deleted_at:
                raise HTTPException(status_code=404, detail="Order not found.")

            order.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(order)

            logger.info("Order %s soft deleted", order_id)
            return order

    except SQLAlchemyError as e:
        logger.error("Error soft deleting order: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Database error while deleting order.")
