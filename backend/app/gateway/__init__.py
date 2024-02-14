from fastapi import APIRouter

from .pupils import router as pupils


router = APIRouter()

router.include_router(pupils, tags=["Ученики"])
