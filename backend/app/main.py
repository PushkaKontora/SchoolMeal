from fastapi import FastAPI

from app.auth.api import AuthAPI
from app.cancel_meal_periods.api import CancelMealPeriodsAPI
from app.children.api import ChildrenAPI
from app.config import AppSettings, SignedRequestSettings
from app.database.container import Database
from app.exceptions import APIException, handle_api_exception
from app.middlewares import SignatureMiddleware
from app.users.api import UsersAPI


def create_app() -> FastAPI:
    settings = AppSettings()
    signature_settings = SignedRequestSettings()

    database = Database()
    database.wire(packages=["app"])

    app_ = FastAPI(debug=settings.debug, docs_url="/docs" if settings.debug else None)
    app_.add_exception_handler(APIException, handle_api_exception)
    app_.add_middleware(SignatureMiddleware, settings=signature_settings)

    auth = AuthAPI()
    app_.include_router(auth.router())

    users = UsersAPI(password_service=auth.password_service, jwt_auth=auth.jwt_auth)
    app_.include_router(users.router())

    children = ChildrenAPI(jwt_auth=auth.jwt_auth)
    app_.include_router(children.router())

    periods = CancelMealPeriodsAPI(jwt_auth=auth.jwt_auth)
    app_.include_router(periods.router())

    return app_


app = create_app()
