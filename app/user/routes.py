from fastapi import APIRouter, HTTPException, status

from app.user.dto import UserCreate, UserWithProfiles
from app.user.model import User
from app.user.services import (
    create_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    hard_delete_user,
    soft_delete_user,
)

user_router = APIRouter(prefix="/users")


@user_router.get("/", response_model=None, status_code=status.HTTP_200_OK)
async def list_users():
    return get_all_users()


@user_router.post("/", response_model=None, status_code=status.HTTP_200_OK)
async def register_user(user: UserCreate):
    is_registered = get_user_by_email(user.email)

    if is_registered is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    return create_user(user)


# @user_router.delete("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
# async def delete_user(user_id: int):
#     is_deleted = soft_delete_user(user_id)

#     if not is_deleted:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     return is_deleted


# @user_router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
# async def get_user(user_id: int):
#     user = get_user_by_id(user_id)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     return user


# @user_router.delete(
#     "/{user_id}/hard", response_model=User, status_code=status.HTTP_200_OK
# )
# async def delete_user_hard(user_id: int):
#     success = hard_delete_user(user_id)

#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     return success
