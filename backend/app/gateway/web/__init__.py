from fastapi import APIRouter

from .requests.routes import router as requests
from .school_classes.routes import router as school_classes


router = APIRouter(prefix="/web")

router.include_router(requests)
router.include_router(school_classes)
