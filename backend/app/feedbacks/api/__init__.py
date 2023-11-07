from fastapi import APIRouter

from .routers import router as feedback_router


router = APIRouter()

router.include_router(feedback_router, prefix="/canteens/{canteen_id}", tags=["Отзыв о столовой"])
