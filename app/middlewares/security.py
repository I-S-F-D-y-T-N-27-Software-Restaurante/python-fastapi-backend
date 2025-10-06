"""
Security utilities for FastAPI with JWT authentication
"""

import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.types import Roles

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="your secret key").encode("utf-8")

# Configurar HTTPBearer para Swagger UI
security = HTTPBearer()


async def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Dependency para obtener el usuario actual desde el token JWT
    Esta función es compatible con Swagger UI
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[os.getenv("ALGORITHM", "HS256")]
        )

        user_id = payload.get("user_id")
        email = payload.get("sub")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: datos de usuario faltantes",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": user_id,
            "sub": email,
            "roles": payload.get("roles", []),
        }

    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err


def role_required(role: str | Roles):
    def dependency(token=Depends(get_current_user_token)):
        user_roles = token["roles"]
        if not user_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No roles in token"
            )
        print(user_roles)
        if role not in user_roles and "admin" not in user_roles:  # admin override
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges"
            )
        return token

    return dependency
