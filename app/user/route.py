import logging
import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import SQLAlchemyError

from app.config.types import Roles
from app.middlewares.auth import get_current_user
from app.middlewares.security import role_required
from app.user.dto import UserBaseDTO, UserCreateDTO, UserDeleteDTO
from app.user.services import (
    create_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    hard_delete_user,
    restore_user,
    soft_delete_user,
)

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/users", tags=["Users"])


# Dependency personalizado para logging de operaciones sensibles
async def log_sensitive_operation(
    request: Request, current_user: dict = Depends(get_current_user)
):
    """Middleware/dependency para operaciones sensibles de usuarios"""
    start_time = time.time()

    # Log de la operación
    operation = f"{request.method} {request.url.path}"
    logger.info(
        f"Operación sensible iniciada: {operation} por usuario {current_user['user_id']} ({current_user['sub']})"
    )

    return {
        "user_id": current_user["user_id"],
        "user_email": current_user["sub"],
        "operation": operation,
        "start_time": start_time,
    }


@user_router.get(
    "/",
    response_model=List[UserBaseDTO],
    status_code=status.HTTP_200_OK,
    summary="List all users",
    description="Retrieve a list of all users in the system",
)
async def list_users():
    return get_all_users()


@user_router.post(
    "/",
    response_model=UserBaseDTO,
    status_code=status.HTTP_200_OK,
    summary="Register a new user",
    description="Create a new user account with the provided information",
)
async def register_user(
    user: UserCreateDTO,
    _=Depends(role_required(Roles.ADMIN)),
):
    is_registered = get_user_by_email(user.email)

    if is_registered is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    return create_user(user)


@user_router.delete(
    "/{user_id}",
    response_model=UserDeleteDTO,
    status_code=status.HTTP_200_OK,
    summary="Soft delete user",
    description="Mark a user as deleted without removing from database",
)
async def delete_user(user_id: int, _=Depends(role_required(Roles.ADMIN))):
    is_deleted = soft_delete_user(user_id)

    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return is_deleted


@user_router.get(
    "/{user_id}",
    response_model=UserBaseDTO,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Retrieve a single user by their unique ID",
)
async def get_user(user_id: int):
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@user_router.delete(
    "/{user_id}/hard",
    response_model=UserBaseDTO,
    status_code=status.HTTP_200_OK,
    summary="Hard delete user",
    description="Permanently remove a user from the database",
)
async def delete_user_hard(user_id: int, _=Depends(role_required(Roles.ADMIN))):
    success = hard_delete_user(user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return success


@user_router.post(
    "/{user_id}/restore",
    response_model=UserBaseDTO,
    status_code=status.HTTP_200_OK,
    summary="Restore deleted user",
    description="Restore a previously soft-deleted user (requires admin privileges)",
)
def restore_user_endpoint(
    user_id: str,
    log_info: dict = Depends(
        log_sensitive_operation,
    ),
    _=Depends(role_required(Roles.ADMIN)),
):
    """Restaurar un usuario eliminado - CON middleware de operación sensible"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido",
            )

        logger.info(
            f"Restaurando usuario {user_id} - User: {log_info['user_id']} ({log_info['user_email']}), Operation: {log_info['operation']}"
        )
        return restore_user(user_id)
    except HTTPException:
        raise
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al restaurar el usuario",
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al restaurar el usuario",
        ) from error
