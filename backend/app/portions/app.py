from fastapi import FastAPI

from app.portions.presentation.routers import get_portions_router


def register_portions_api(app: FastAPI) -> None:
    app.include_router(
        router=get_portions_router(),
        prefix="/portions",
        tags=["portions"],
    )
