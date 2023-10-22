from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.legacy.auth.app import register_auth_api
from app.legacy.cancel_meal_periods.app import register_cancel_meal_periods_api
from app.legacy.children.app import register_children_api
from app.legacy.container import AppContainer
from app.legacy.meal_requests.app import register_meal_requests_api
from app.legacy.meals.app import register_meals_api
from app.legacy.portions.app import register_portions_api
from app.legacy.school_classes.app import register_school_classes_api
from app.legacy.users.app import register_users_api
from app.legacy.utils.error import Error, handle_api_error


def create_app() -> FastAPI:
    container = AppContainer()

    app_settings = container.app_settings()

    application = FastAPI(docs_url=app_settings.docs_url)
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


def _add_middlewares(application: FastAPI, container: AppContainer) -> None:
    cors_settings = container.cors_settings()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=cors_settings.origins,
        allow_credentials=cors_settings.allow_credentials,
        allow_methods=cors_settings.methods,
        allow_headers=cors_settings.headers,
    )


app = create_app()
