from fastapi import APIRouter

from .requests.routes import router as requests


router = APIRouter(prefix="/web")

router.include_router(requests)
