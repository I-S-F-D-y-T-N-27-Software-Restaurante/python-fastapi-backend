from typing import List

from fastapi import APIRouter, HTTPException, status

from app.config.types import UserProfileEnum
from app.resto.dto import UserBaseWithRestoProfilesDTO
from app.resto.services import get_all_employees, get_employee_by_id, make_user_role

resto_router = APIRouter(prefix="/resto")


@resto_router.get(
    "/",
    response_model=List[UserBaseWithRestoProfilesDTO],
    status_code=status.HTTP_200_OK,
)
async def list_users():
    return get_all_employees()


@resto_router.post(
    "/roles/{user_id}/{role}",
    response_model=UserBaseWithRestoProfilesDTO,
    status_code=status.HTTP_200_OK,
)
async def make_user_profile(user_id: str, role: UserProfileEnum):
    user = get_employee_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found.",
        )

    return make_user_role(user, role)
