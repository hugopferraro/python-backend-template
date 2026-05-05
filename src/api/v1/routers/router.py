from fastapi import APIRouter
from src.api.v1.routers.security.auth_route import router as auth_router
from src.api.v1.routers.user import router as user_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(auth_router)
