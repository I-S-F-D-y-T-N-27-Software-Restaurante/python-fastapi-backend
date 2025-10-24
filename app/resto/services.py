import logging
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.config.cnx import SessionLocal
from app.config.sql_models import Cashier, Cook, User, Waiter, Order, OrderItem, OrderStatus, RestorantTable
from app.config.types import Roles
from app.resto.dto import OrderCreateDTO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ===================================================
#               EMPLEADOS
# ===================================================

def get_all_employees():
    """Busca y retorna todos los usuarios con perfiles de cocina activos."""
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
    """Obtiene un empleado por su ID."""
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
            raise HTTPException(status_code=400, detail="Employee not found.")
        return user


def get_employee_by_email(email: str):
    """Busca y retorna un usuario por email."""
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
    """Asigna un rol a un usuario (waiter, cook o cashier)."""
    with SessionLocal() as db:
        try:
            if role == Roles.WAITER:
                if user.waiter_profile is not None:
                    raise HTTPException(status_code=400, detail="Usuario ya es mesero.")
                db.add(Waiter(user=user))

            elif role == Roles.COOK:
                if user.cook_profile is not None:
                    raise HTTPException(status_code=400, detail="Usuario ya es cocinero.")
                db.add(Cook(user=user))

            elif role == Roles.CASHIER:
                if user.cashier_profile is not None:
                    raise HTTPException(status_code=400, detail="Usuario ya es cajero.")
                db.add(Cashier(user=user))

            db.commit()
            db.refresh(user)
            return user

        except SQLAlchemyError as e:
            db.rollback()
            logger.error("Error al crear perfil: %s", e, exc_info=True)
            raise


# ===================================================
#               PEDIDOS
# ===================================================

def create_order(order_data: OrderCreateDTO):
    """Crea un nuevo pedido y sus items."""
    with SessionLocal() as db:
        try:
            new_order = Order(
                table_id=order_data.table_id,
                waiter_id=order_data.waiter_id,
                status_id=order_data.status_id or 1,  # Estado inicial
                total_amount=Decimal("0.00"),
                created_at=datetime.now(timezone.utc),
            )

            db.add(new_order)
            db.flush()  # Genera el ID del pedido antes de crear items

            total = Decimal("0.00")
            for item in order_data.items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                )
                db.add(order_item)
                total += item.price * item.quantity

            new_order.total_amount = total
            db.commit()
            db.refresh(new_order)
            return new_order

        except SQLAlchemyError as e:
            db.rollback()
            logger.error("Error al crear pedido: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail="Error al crear el pedido.")


def get_order_by_id(order_id: int):
    """Obtiene un pedido por su ID."""
    with SessionLocal() as db:
        order = (
            db.query(Order)
            .options(selectinload(Order.items))
            .filter(Order.id == order_id, Order.deleted_at.is_(None))
            .first()
        )
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        return order


def list_all_orders():
    """Lista todos los pedidos activos."""
    with SessionLocal() as db:
        orders = (
            db.query(Order)
            .options(selectinload(Order.items))
            .filter(Order.deleted_at.is_(None))
            .all()
        )
        return orders


def update_order_status(order_id: int, status_id: int):
    """Actualiza el estado de un pedido."""
    with SessionLocal() as db:
        order = db.query(Order).filter(Order.id == order_id, Order.deleted_at.is_(None)).first()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")

        status_obj = db.query(OrderStatus).filter(OrderStatus.id == status_id).first()
        if not status_obj:
            raise HTTPException(status_code=400, detail="Estado inválido.")

        order.status_id = status_id
        db.commit()
        db.refresh(order)
        return order


def soft_delete_order(order_id: int):
    """Elimina lógicamente un pedido."""
    with SessionLocal() as db:
        order = db.query(Order).filter(Order.id == order_id, Order.deleted_at.is_(None)).first()
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")

        order.deleted_at = datetime.now(timezone.utc)
        db.commit()
        return order