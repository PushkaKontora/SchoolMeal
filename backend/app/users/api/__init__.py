from fastapi import APIRouter

from .jwt.routers import router as jwt_router
from .registration.routers import router as registration_router
from .user.routers import router as user_router


router = APIRouter()

router.include_router(jwt_router, prefix="", tags=["Аутентификация и JWT"])
router.include_router(registration_router, prefix="", tags=["Регистрация"])
router.include_router(user_router, prefix="", tags=["Действия с аккаунтом"])
