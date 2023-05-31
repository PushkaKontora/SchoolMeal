from fastapi import FastAPI

from app.auth.app import register_auth_api
from app.cancel_meal_periods.app import register_cancel_meal_periods_api
from app.children.app import register_children_api
from app.config import Environment
from app.container import Container
from app.meal_requests.app import register_meal_requests_api
from app.meals.app import register_meals_api
from app.portions.app import register_portions_api
from app.school_classes.app import register_school_classes_api
from app.users.app import register_users_api
from app.utils.error import Error, handle_api_error
from app.utils.middlewares import RequestSignatureMiddleware


def create_app() -> FastAPI:
    container = Container()
    settings = container.app_settings()

    application = FastAPI(debug=settings.debug, docs_url=settings.docs_url if settings.debug else None)
    application.add_exception_handler(Error, handle_api_error)

    if settings.environment == Environment.PRODUCTION:
        application.add_middleware(RequestSignatureMiddleware, settings=container.request_signature_settings())

    registers = (
        register_auth_api,
        register_cancel_meal_periods_api,
        register_children_api,
        register_meals_api,
        register_portions_api,
        register_users_api,
        register_school_classes_api,
        register_meal_requests_api,
    )
    for register in registers:
        register(application)

    return application


app = create_app()
