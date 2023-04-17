from typing import Iterable

from dependency_injector.providers import Factory
from fastapi import APIRouter, FastAPI

from app.auth.api import AuthAPI
from app.config import AppSettings
from app.database.container import Database
from app.exceptions import ExceptionHandler


def create_app() -> FastAPI:
    settings = AppSettings()

    database = Database()
    database.wire(packages=["app"])

    app = FastAPI(debug=settings.debug, docs_url="/docs" if settings.debug else None)

    apis = [AuthAPI]
    for api in apis:
        instance = api()
        router: APIRouter = instance.router()
        exceptions_handlers = instance.exceptions_handlers()

        app.include_router(router)
        for handler in exceptions_handlers:
            app.add_exception_handler(handler.exception, handler.handle)

    return app


app = create_app()
