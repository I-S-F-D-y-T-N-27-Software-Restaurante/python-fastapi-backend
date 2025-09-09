from fastapi import APIRouter

from app.user.route import user_router

api_router = APIRouter()


@api_router.get("/")
async def root():
    return {"message": "Hello World"}


@api_router.get("/health")
async def health_check():
    return {"status": "ok"}


api_router.include_router(user_router)
