import logging
import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.exc import SQLAlchemyError

from app.config.types import Roles
from app.middlewares.auth import get_current_user
from app.middlewares.security import get_current_user_token, role_required
from app.resto.services import get_employee_by_id
from app.user.dto import (
    TokenDTO,
    UserBaseDTO,
    UserCreateDTO,
    UserDeleteDTO,
    UserLoginDTO,
    UserTokenDataDTO,
)
from app.user.services import (
    create_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    hard_delete_user,
    login_user,
    restore_user,
    soft_delete_user,
)

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/users")


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


@user_router.get("/", response_model=List[UserBaseDTO], status_code=status.HTTP_200_OK)
async def list_users():
    return get_all_users()


@user_router.post(
    "/",
    response_model=UserBaseDTO,
    status_code=status.HTTP_200_OK,
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
    "/{user_id}", response_model=UserDeleteDTO, status_code=status.HTTP_200_OK
)
async def delete_user(user_id: int, _=Depends(role_required(Roles.ADMIN))):
    is_deleted = soft_delete_user(user_id)

    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return is_deleted


@user_router.get("/me", response_model=UserTokenDataDTO, status_code=status.HTTP_200_OK)
def get_current_user_profile(current_user: dict = Depends(get_current_user_token)):
    """Obtener perfil del usuario actual"""
    try:
        user_id = current_user["user_id"]
        user = get_employee_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return current_user

    except HTTPException:
        raise
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener el perfil",
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el perfil",
        ) from error


@user_router.get(
    "/{user_id}", response_model=UserBaseDTO, status_code=status.HTTP_200_OK
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
    "/{user_id}/hard", response_model=UserBaseDTO, status_code=status.HTTP_200_OK
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
    "/{user_id}/restore", response_model=UserBaseDTO, status_code=status.HTTP_200_OK
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


@user_router.post("/login", response_model=TokenDTO, status_code=status.HTTP_200_OK)
def login_endpoint(response: Response, login_data: UserLoginDTO):
    """Login de usuario - SIN middleware (acceso público)"""
    try:
        token_data = login_user(login_data.email, login_data.password)

        response.set_cookie(
            key="token",
            value=token_data["access_token"],
            httponly=True,
            secure=False,
            path="/",
            samesite="lax",
            max_age=3600,
            domain="localhost",
        )

        return token_data

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al iniciar sesión",
        ) from e


@user_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(response: Response):
    return response.delete_cookie(
        key="token",
        path="/",
        httponly=True,
        secure=False,
        samesite="lax",
        domain="localhost",
    )
