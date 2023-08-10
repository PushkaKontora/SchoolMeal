from fastapi import FastAPI

from app.legacy.auth.presentation.routers import get_auth_router


def register_auth_api(app: FastAPI) -> None:
    app.include_router(
        router=get_auth_router(),
        prefix="/auth",
        tags=["auth"],
    )
