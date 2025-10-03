import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", "your secret key").encode("utf-8")

# Rutas públicas (no requieren token)
PUBLIC_ROUTES = [
    "/",
    "/home",
    "/test",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
]

# Rutas que requieren métodos específicos pero no autenticación
PUBLIC_METHODS = {
    "/api/users": ["POST"],  # Registro público
    "/api/users/login": ["POST", "OPTIONS"],  # Login público
    "/api/health": ["GET"],
}

# Rutas que requieren autenticación pero no verificación de permisos
AUTHENTICATED_ONLY_ROUTES = [
    "/api/users/me",
]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def compare_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=os.getenv("ALGORITHM", "HS256"))


def verify_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, SECRET_KEY, algorithms=[os.getenv("ALGORITHM", "HS256")]
        )
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Token expirado") from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail="Token inválido") from err


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._permission_service = None

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method

        if self.is_public_route(path, method):
            return await call_next(request)

        authorization: Optional[str] = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=401, content={"detail": "Token de autorización requerido"}
            )

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Esquema inválido. Use 'Bearer <token>'"},
                )

            payload = verify_jwt_token(token)
            request.state.user = payload

            # Aquí puedes agregar verificación de permisos si quieres
        except ValueError:
            return JSONResponse(
                status_code=401, content={"detail": "Formato de token inválido"}
            )
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception:
            return JSONResponse(
                status_code=401, content={"detail": "Error de autenticación"}
            )

        return await call_next(request)

    def is_public_route(self, path: str, method: str) -> bool:
        # Rutas completamente públicas
        if path in PUBLIC_ROUTES:
            return True
        # Rutas con métodos específicos públicos
        for route, methods in PUBLIC_METHODS.items():
            if path.startswith(route) and method in methods:
                return True
        # Prefijos para documentación
        for prefix in ["/docs", "/redoc"]:
            if path.startswith(prefix):
                return True
        return False


# OAuth2 y dependencias para endpoints individuales
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(
            token, SECRET_KEY, algorithms=[os.getenv("ALGORITHM", "HS256")]
        )
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado"
        ) from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        ) from err


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = await verify_token(token)
    user_id = payload.get("user_id")
    email = payload.get("sub")
    if not user_id or not email:
        raise HTTPException(status_code=401, detail="Token inválido: datos faltantes")
    return {
        "user_id": user_id,
        "sub": email,
        "roles": payload.get("roles", []),
        "permissions": payload.get("permissions", []),
    }
