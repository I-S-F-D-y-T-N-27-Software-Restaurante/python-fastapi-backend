from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Request

from app.user.dto import UserBaseDTO, UserLogin, UserCreateDTO, UserDeleteDTO, UserUpdateDTO, UserInsertDTO, Token, UserOut
from app.user.services import (
    create_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    insert_user,
    update_user,
    hard_delete_user,
    soft_delete_user,
    login_user,
    restore_user
)
from app.middlewares.auth import get_current_user
from app.middlewares.security import get_current_user_token
import logging
import time
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/users")

# Dependency personalizado para logging de operaciones sensibles
async def log_sensitive_operation(request: Request, current_user: dict = Depends(get_current_user)):
    """Middleware/dependency para operaciones sensibles de usuarios"""
    start_time = time.time()
    
    # Log de la operación
    operation = f"{request.method} {request.url.path}"
    logger.info(f"Operación sensible iniciada: {operation} por usuario {current_user['user_id']} ({current_user['sub']})")
    
    return {
        "user_id": current_user["user_id"],
        "user_email": current_user["sub"], 
        "operation": operation,
        "start_time": start_time
    }

@user_router.get("/", response_model=List[UserBaseDTO], status_code=status.HTTP_200_OK)
async def list_users():
    return get_all_users()


@user_router.post("/", response_model=UserBaseDTO, status_code=status.HTTP_200_OK)
async def register_user(user: UserCreateDTO):
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
async def delete_user(user_id: int):
    is_deleted = soft_delete_user(user_id)

    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return is_deleted

@user_router.get('/me', response_model=UserOut, status_code=status.HTTP_200_OK)
def get_current_user_profile(current_user: dict = Depends(get_current_user_token)):
    """Obtener perfil del usuario actual"""
    try:
        user_id = current_user["user_id"]
        user = get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
            
        return user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al obtener el perfil"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al obtener el perfil"
        )


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
async def delete_user_hard(user_id: int):
    success = hard_delete_user(user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    return success

@user_router.post('/{user_id}/restore', response_model=UserOut, status_code=status.HTTP_200_OK)
def restore_user_endpoint(user_id: str, log_info: dict = Depends(log_sensitive_operation)):
    """Restaurar un usuario eliminado - CON middleware de operación sensible"""
    try:
        if not user_id or not user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID de usuario es requerido"
            )
        
        logger.info(
            f"Restaurando usuario {user_id} - User: {log_info['user_id']} ({log_info['user_email']}), Operation: {log_info['operation']}"
        )
        return restore_user(user_id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor al restaurar el usuario"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al restaurar el usuario"
        )


@user_router.post('/login', response_model=Token, status_code=status.HTTP_200_OK)
def login_endpoint(login_data: UserLogin):
    """Login de usuario - SIN middleware (acceso público)"""
    try:
        return login_user(login_data.email, login_data.password)  # Cambiado de emails a email
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error inesperado al iniciar sesión"
        )