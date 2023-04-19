from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, List, Singleton

from app.auth.domain.services import AuthService, JWTService, PasswordService
from app.auth.presentation.handlers import (
    AuthHandlers,
    BadCredentialsHandler,
    InvalidBearerCredentialsHandler,
    InvalidTokenSignatureHandler,
    NotFoundRefreshCookieHandler,
    NotFoundRefreshTokenHandler,
    RefreshWithRevokedTokenHandler,
    TokenExpirationHandler,
    UnauthorizedHandler,
)
from app.auth.presentation.middlewares import JWTAuth
from app.auth.presentation.routers import AuthRouter
from app.config import JWTSettings, PasswordSettings


class AuthAPI(DeclarativeContainer):
    jwt_settings = Singleton(JWTSettings)
    password_settings = Singleton(PasswordSettings)

    jwt_service = Factory(JWTService, jwt_settings=jwt_settings)
    password_service = Factory(PasswordService, password_settings=password_settings)
    auth_service = Factory(AuthService, password_service=password_service, jwt_service=jwt_service)

    auth_handlers = Factory(AuthHandlers, auth_service=auth_service, jwt_settings=jwt_settings)
    exceptions_handlers = List(
        Factory(BadCredentialsHandler),
        Factory(NotFoundRefreshCookieHandler),
        Factory(InvalidTokenSignatureHandler),
        Factory(NotFoundRefreshTokenHandler),
        Factory(TokenExpirationHandler),
        Factory(RefreshWithRevokedTokenHandler),
        Factory(InvalidBearerCredentialsHandler),
        Factory(UnauthorizedHandler),
    )

    jwt_auth = Factory(JWTAuth, jwt_service=jwt_service)

    router = Factory(AuthRouter, auth_handlers=auth_handlers)
