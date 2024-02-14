from fastapi import APIRouter

from .pupils import router as pupils
from .requests import router as requests


router = APIRouter()

router.include_router(pupils, tags=["Ученики"])
router.include_router(requests, tags=["Заявки"])
