from fastapi import APIRouter, FastAPI

from app.auth.api import AuthAPI
from app.config import AppSettings
from app.database.container import Database


def create_app() -> FastAPI:
    settings = AppSettings()

    database = Database()
    database.wire(packages=["app"])

    app_ = FastAPI(debug=settings.debug, docs_url="/docs" if settings.debug else None)

    apis = [AuthAPI]
    for api in apis:
        instance = api()
        router: APIRouter = instance.router()
        exceptions_handlers = instance.exceptions_handlers()

        app_.include_router(router)
        for handler in exceptions_handlers:
            app_.add_exception_handler(handler.exception, handler.handle)

    return app_


app = create_app()
