from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

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
    summary="Convert a user into an employee of a specific type",
    description="Endpoint for an admin to assign a role to a user/employee.",
)
async def make_user_profile(
    user_id: int,
    role: Roles,
    _=Depends(role_required(Roles.ADMIN)),
):
    try:
        user = get_employee_by_id(user_id)
        return make_user_role(user, role)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to assign role to user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


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
