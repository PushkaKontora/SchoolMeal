from fastapi import APIRouter

from .auth import router as auth
from .mobile import router as mobile
from .web import router as web


router = APIRouter()

router.include_router(auth, prefix="/auth")
router.include_router(mobile, prefix="/mobile")
router.include_router(web, prefix="/web")
