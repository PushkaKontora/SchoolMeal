from fastapi import APIRouter

from .feedbacks.routes import router as feedbacks
from .pupils.routes import router as pupils


router = APIRouter(prefix="/mobile")


router.include_router(pupils)
router.include_router(feedbacks)
