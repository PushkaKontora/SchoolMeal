from fastapi import FastAPI

from app.children.presentation.routers import get_children_router


def register_children_api(app: FastAPI) -> None:
    app.include_router(
        router=get_children_router(),
        prefix="/children",
        tags=["children"],
    )
