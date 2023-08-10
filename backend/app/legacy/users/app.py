from fastapi import FastAPI

from app.legacy.users.presentation.routers import get_users_router


def register_users_api(app: FastAPI) -> None:
    app.include_router(
        router=get_users_router(),
        prefix="/users",
        tags=["users"],
    )
