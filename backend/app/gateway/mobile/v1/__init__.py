from fastapi import APIRouter

from .feedbacks.routes import router as feedbacks
from .pupils.routes import router as pupils


router = APIRouter()

router.include_router(feedbacks)
router.include_router(pupils)
