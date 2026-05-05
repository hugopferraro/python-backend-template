from fastapi import APIRouter

from . import (create_user_route,delete_user_route,
               get_me_route, get_user_route,
               list_users_route, update_user_route)

router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(create_user_route.router)
router.include_router(get_me_route.router)
router.include_router(list_users_route.router)
router.include_router(get_user_route.router)
router.include_router(update_user_route.router)
router.include_router(delete_user_route.router)
