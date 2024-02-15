from fastapi import APIRouter

from .requests import router as requests


router = APIRouter(prefix="/web")

router.include_router(requests, tags=["Заявки"])
