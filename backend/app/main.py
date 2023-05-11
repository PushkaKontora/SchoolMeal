from fastapi import FastAPI

from app.auth.app import register_auth_api
from app.cancel_meal_periods.app import register_cancel_meal_periods_api
from app.children.app import register_children_api
from app.config import RequestSignatureSettings
from app.container import Container
from app.database.container import Database
from app.exceptions import APIException, handle_api_exception
from app.meals.app import register_meals_api
from app.middlewares import RequestSignatureMiddleware
from app.portions.app import register_portions_api
from app.users.app import register_users_api


def create_app() -> FastAPI:
    container = Container()
    settings = container.app_settings()

    database = Database()
    database.wire(packages=["app"])

    application = FastAPI(debug=settings.debug, docs_url="/docs" if settings.debug else None)
    application.add_exception_handler(APIException, handle_api_exception)

    if not settings.debug:
        application.add_middleware(RequestSignatureMiddleware, settings=container.request_signature_settings())

    registers = (
        register_auth_api,
        register_cancel_meal_periods_api,
        register_children_api,
        register_meals_api,
        register_portions_api,
        register_users_api,
    )
    for register in registers:
        register(application)

    return application


app = create_app()
