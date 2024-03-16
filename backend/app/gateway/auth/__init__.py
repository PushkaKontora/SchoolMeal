from fastapi import APIRouter

from .v1.routes import router as v1


router = APIRouter()

router.include_router(v1, prefix="/v1", tags=["Auth API v1"])
