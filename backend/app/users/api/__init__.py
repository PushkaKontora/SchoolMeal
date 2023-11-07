from fastapi import APIRouter

from .jwt.routers import router as jwt_router
from .registration.routers import router as registration_router
from .user.routers import router as user_router


router = APIRouter(prefix="/users")

router.include_router(jwt_router, tags=["Аутентификация и JWT"])
router.include_router(registration_router, tags=["Регистрация"])
router.include_router(user_router, tags=["Действия с аккаунтом"])
