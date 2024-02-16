from fastapi import APIRouter

from .feedbacks import router as feedbacks
from .pupils import router as pupils


router = APIRouter(prefix="/mobile")


router.include_router(pupils, tags=["Ученики"])
router.include_router(feedbacks, tags=["Отзывы"])
