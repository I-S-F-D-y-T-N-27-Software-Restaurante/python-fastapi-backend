import logging

from sqlalchemy.orm import selectinload

from app.config.cnx import SessionLocal
from app.config.sql_models import User
from app.config.types import Roles
from app.middlewares.auth import compare_password, create_access_token

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def authenticate_user(email: str, password: str):
    """Autenticar un usuario por email y contraseña"""
    try:
        with SessionLocal() as db:
            if not email or not password:
                return None

            logger.info(f"DEBUG here: {password} {email}")

            user = (
                db.query(User)
                .options(
                    selectinload(User.waiter_profile),
                    selectinload(User.cook_profile),
                    selectinload(User.cashier_profile),
                )
                .filter(User.email == email, User.deleted_at.is_(None))
                .first()
            )

            if not user or not compare_password(password, user.password):
                logger.warning(f"Intento de autenticación fallido para email: {email}")
                return None

            logger.info(f"Usuario autenticado exitosamente: {user.email}")
            return user

    except Exception as e:
        logger.error(f"Error inesperado al autenticar usuario: {str(e)}")
        return None
    finally:
        if db:
            db.close()


def login_user(email: str, password: str):
    """Login de usuario y generación de token"""
    user = authenticate_user(email, password)

    if not user:
        raise ValueError("Credenciales inválidas")

    roles = []

    if user.cashier_profile:
        roles.append(Roles.CASHIER)
    if user.cook_profile:
        roles.append(Roles.COOK)
    if user.waiter_profile:
        roles.append(Roles.WAITER)

    # assign admin privileges to single user for mock pourposes
    if user.email == "evan@example.com":
        roles.append("admin")  # type: ignore

    # Generar token
    token_data = {"sub": user.email, "user_id": str(user.id), "roles": roles}

    access_token = create_access_token(data=token_data)

    logger.info(f"Login exitoso para usuario: {user.email}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "user_email": user.email,
        "roles": roles,
    }
