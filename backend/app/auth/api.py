from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, List, Singleton

from app.auth.domain.services import AuthService, JWTService, PasswordsService
from app.auth.presentation.handlers import AuthHandlers, BadCredentialsHandler
from app.auth.presentation.routers import AuthRouter
from app.config import JWTSettings
from app.exceptions import DomainExceptionHandler


class AuthAPI(DeclarativeContainer):
    jwt_settings = Singleton(JWTSettings)

    jwt_service = Factory(JWTService, jwt_settings=jwt_settings)
    passwords_service = Factory(PasswordsService)
    auth_service = Factory(AuthService, passwords_service=passwords_service, jwt_service=jwt_service)

    auth_handlers = Factory(AuthHandlers, auth_service=auth_service, jwt_settings=jwt_settings)
    exceptions_handlers: List[Factory[DomainExceptionHandler]] = List(Factory(BadCredentialsHandler))

    router = Factory(AuthRouter, auth_handlers=auth_handlers)