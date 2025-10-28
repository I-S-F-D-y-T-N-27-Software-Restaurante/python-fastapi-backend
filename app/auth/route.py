import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError

from app.auth.dto import TokenDTO, UserLoginDTO, UserTokenDataDTO
from app.auth.services import login_user
from app.middlewares.security import get_current_user_token
from app.resto.services import get_employee_by_id

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.get(
    "/me",
    response_model=UserTokenDataDTO,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Retrieve the profile data of the currently authenticated user",
)
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


@auth_router.post(
    "/login",
    response_model=TokenDTO,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate a user and issue a JWT token. Public route, no authentication required",
)
def login_endpoint(response: Response, login_data: UserLoginDTO):
    """Login de usuario - SIN middleware (acceso público)"""
    try:
        token_data = login_user(login_data.email, login_data.password)

        response.set_cookie(
            key="RESTOApiToken",
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


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="User logout",
    description="Invalidate the current user session by deleting the HTTP-only JWT cookie",
)
def logout_user(response: Response):
    return response.delete_cookie(
        key="RESTOApiToken",
        path="/",
        httponly=True,
        secure=False,
        samesite="lax",
        domain="localhost",
    )
