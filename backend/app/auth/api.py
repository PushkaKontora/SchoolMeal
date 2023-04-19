from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, List, Singleton

from app.auth.domain.services import AuthService, JWTService, PasswordService
from app.auth.presentation.handlers import (
    AuthHandlers,
    BadCredentialsHandler,
    InvalidTokenSignatureHandler,
    NotFoundRefreshCookieHandler,
    NotFoundRefreshTokenHandler,
    RefreshWithRevokedTokenHandler,
    TokenExpirationHandler,
)
from app.auth.presentation.routers import AuthRouter
from app.config import JWTSettings, PasswordSettings
from app.exceptions import ExceptionHandler


class AuthAPI(DeclarativeContainer):
    jwt_settings = Singleton(JWTSettings)
    password_settings = Singleton(PasswordSettings)

    jwt_service = Factory(JWTService, jwt_settings=jwt_settings)
    password_service = Factory(PasswordService, password_settings=password_settings)
    auth_service = Factory(AuthService, password_service=password_service, jwt_service=jwt_service)

    auth_handlers = Factory(AuthHandlers, auth_service=auth_service, jwt_settings=jwt_settings)
    exceptions_handlers: List[Factory[ExceptionHandler]] = List(
        Factory(BadCredentialsHandler),
        Factory(NotFoundRefreshCookieHandler),
        Factory(InvalidTokenSignatureHandler),
        Factory(NotFoundRefreshTokenHandler),
        Factory(TokenExpirationHandler),
        Factory(RefreshWithRevokedTokenHandler),
    )

    router = Factory(AuthRouter, auth_handlers=auth_handlers)
