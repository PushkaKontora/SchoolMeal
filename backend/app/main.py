from fastapi import APIRouter, FastAPI

from app.auth.api import AuthAPI
from app.config import AppSettings, SignedRequestSettings
from app.database.container import Database
from app.middlewares import SignatureMiddleware
from app.users.api import UsersAPI


def create_app() -> FastAPI:
    settings = AppSettings()
    signature_settings = SignedRequestSettings()

    database = Database()
    database.wire(packages=["app"])

    app_ = FastAPI(debug=settings.debug, docs_url="/docs" if settings.debug else None)
    app_.add_middleware(SignatureMiddleware, settings=signature_settings)

    auth = AuthAPI()
    users = UsersAPI(password_service=auth.password_service, jwt_auth=auth.jwt_auth)

    for api in [auth, users]:
        router: APIRouter = api.router()
        exceptions_handlers = api.exceptions_handlers()

        app_.include_router(router)
        for handler in exceptions_handlers:
            app_.add_exception_handler(handler.exception, handler.handle)

    return app_


app = create_app()
