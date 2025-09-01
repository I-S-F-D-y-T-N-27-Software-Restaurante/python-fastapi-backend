from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .dto.user_create import UserCreate
from .repository import UserRepository

user_router = APIRouter(prefix="/users")


@user_router.get("/")
async def list_users():
    repo = UserRepository()

    users = repo.list_all()

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "users": [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat()
                    if user.updated_at
                    else None,
                }
                for user in users
            ],
        },
    )


@user_router.post("/")
async def create_user(user: UserCreate):
    repo = UserRepository()

    is_registered = repo.get_by_email(user.email)

    if is_registered is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    new_user = repo.create(user)

    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "message": "User created",
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "created_at": new_user.created_at.isoformat(),
            },
        },
    )


@user_router.delete("/{user_id}")
async def delete_user(user_id: int):
    repo = UserRepository()

    success = repo.soft_delete(user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": f"User {user_id} deleted successfully",
        },
    )


@user_router.get("/{user_id}")
async def get_user(user_id: int):
    repo = UserRepository()

    user = repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            },
        },
    )


@user_router.delete("/{user_id}/hard")
async def hard_delete_user(user_id: int):
    repo = UserRepository()

    success = repo.hard_delete(user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": f"User {user_id} deleted successfully",
        },
    )
