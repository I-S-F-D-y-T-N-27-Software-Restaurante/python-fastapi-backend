from fastapi import APIRouter

from app.modules.user.entities import User

user_router = APIRouter()


@user_router.get("/")
async def root():
    return {"message": "Hello World"}


@user_router.post("/users")
async def create_user(user: User):
    return {"message": "User creation endpoint", "user": user.dict()}
