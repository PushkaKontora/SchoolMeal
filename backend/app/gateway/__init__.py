from fastapi import APIRouter

from app.gateway.mobile import router as mobile
from app.gateway.web import router as web


router = APIRouter()

router.include_router(mobile, tags=["Mobile API"])
router.include_router(web, tags=["Web API"])
