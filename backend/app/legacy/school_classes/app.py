from fastapi import FastAPI

from app.legacy.school_classes.presentation.routers import get_school_classes_router


def register_school_classes_api(app: FastAPI) -> None:
    app.include_router(router=get_school_classes_router(), prefix="/school-classes", tags=["School Classes"])
