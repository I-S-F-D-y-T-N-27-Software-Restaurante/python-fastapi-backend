from fastapi import APIRouter

from app.auth.route import auth_router
from app.menu.route import menu_router
from app.resto.route import resto_router
from app.tables.route import tables_router
from app.user.route import user_router

api_router = APIRouter()


@api_router.get("/")
async def root():
    return {"message": "RESTO Backend API"}


@api_router.get("/health")
async def health_check():
    return {"status": "ok"}


api_router.include_router(user_router)
api_router.include_router(resto_router)
api_router.include_router(tables_router)
api_router.include_router(auth_router)
api_router.include_router(menu_router)
