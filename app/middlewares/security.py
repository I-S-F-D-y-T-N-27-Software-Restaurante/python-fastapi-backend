"""
Security utilities for FastAPI with JWT authentication
"""

import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import SECRET_KEY
from app.config.types import Roles

load_dotenv()


security = HTTPBearer(auto_error=False)


def get_current_user_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Get current user from JWT.
    Supports both Authorization header and HTTP-only cookie.
    """
    # Skip auth for preflight requests
    if request.method == "OPTIONS":
        return None

    # First try Bearer token
    token = credentials.credentials if credentials else request.cookies.get("token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # decode the token
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[os.getenv("ALGORITHM", "HS256")]
        )

        user_id = payload.get("user_id")
        email = payload.get("sub")

        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid: missing user data",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": user_id,
            "user_email": email,
            "roles": payload.get("roles", []),
        }

    except jwt.ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err


def role_required(role: str | Roles):
    def dependency(token=Depends(get_current_user_token)):
        user_roles = token["roles"]
        if not user_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="No roles in token"
            )
        if role not in user_roles and "admin" not in user_roles:  # admin override
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges"
            )
        return token

    return dependency
