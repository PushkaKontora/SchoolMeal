from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton

from app.config import AppSettings, DatabaseSettings, JWTSettings, PasswordSettings, RequestSignatureSettings


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    app_settings = Singleton(AppSettings)
    database_settings = Singleton(DatabaseSettings)
    jwt_settings = Singleton(JWTSettings)
    password_settings = Singleton(PasswordSettings)
    request_signature_settings = Singleton(RequestSignatureSettings)
