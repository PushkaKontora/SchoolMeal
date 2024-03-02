from fastapi import APIRouter

from .feedbacks import router as feedbacks
from .pupils import router as pupils


router = APIRouter(prefix="/mobile")


router.include_router(pupils)
router.include_router(feedbacks)
