from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    app_settings = container.app_settings()

    application = FastAPI(debug=app_settings.debug, docs_url=app_settings.docs_url if app_settings.debug else None)
    application.add_exception_handler(Error, handle_api_error)

    _add_middlewares(application, container)
    _register_apis(application)

    return application


def _register_apis(application: FastAPI) -> None:
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


def _add_middlewares(application: FastAPI, container: Container) -> None:
    app_settings = container.app_settings()
    if app_settings.environment == Environment.PRODUCTION:
        application.add_middleware(RequestSignatureMiddleware, settings=container.request_signature_settings())

    cors_settings = container.cors_settings()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=cors_settings.origins,
        allow_credentials=cors_settings.allow_credentials,
        allow_methods=cors_settings.methods,
        allow_headers=cors_settings.headers,
    )


app = create_app()
