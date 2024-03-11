from fastapi import APIRouter

from .mobile import router as mobile
from .web import router as web


router = APIRouter()

router.include_router(mobile, prefix="/mobile")
router.include_router(web, prefix="/web")
