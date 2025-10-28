from typing import List

from fastapi import APIRouter, Depends, status

from app.config.types import Roles
from app.middlewares.security import role_required
from app.resto.dto import UserBaseWithRestoProfilesDTO
from app.resto.services import get_all_employees, get_employee_by_id, make_user_role

resto_router = APIRouter(prefix="/resto", tags=["Restorant"])


@resto_router.get(
    "/roles",
    response_model=List[UserBaseWithRestoProfilesDTO],
    status_code=status.HTTP_200_OK,
    summary="List all users as employees with roles.",
    description="Endpoint only meant for Admin to check current users as Employees: users with their waiter, cook and cashier profile info.",
)
async def list_users(
    _=Depends(role_required(Roles.ADMIN)),
):
    return get_all_employees()


@resto_router.post(
    "/roles/{user_id}/{role}",
    response_model=UserBaseWithRestoProfilesDTO,
    status_code=status.HTTP_200_OK,
    summary="With and UserID converts that user into a employee of type",
    description="Enpoint ment for an admin to assign a role to an user/employee.",
)
async def make_user_profile(
    user_id: int,
    role: Roles,
    _=Depends(role_required(Roles.ADMIN)),
):
    user = get_employee_by_id(user_id)
    return make_user_role(user, role)


@resto_router.get(
    "/roles/{user_id}",
    response_model=UserBaseWithRestoProfilesDTO,
    status_code=status.HTTP_200_OK,
    summary="Gets an User profile as Employee",
    description="Brings User related info with populated profiles for administration pourposes.",
)
async def get_single_user_with_profile(
    user_id: int,
    _=Depends(role_required(Roles.ADMIN)),
):
    return get_employee_by_id(user_id)
