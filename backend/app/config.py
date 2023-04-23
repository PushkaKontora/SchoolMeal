from abc import ABC
from datetime import timedelta
from os.path import join
from pathlib import Path

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from pydantic import BaseSettings, Field, PostgresDsn, SecretStr


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings, ABC):
    class Config:
        env_file = join(BASE_DIR, ".env")


class AppSettings(Settings):
    debug: bool = Field(env="DEBUG")


class DatabaseSettings(Settings):
    driver: str = Field(env="POSTGRES_DRIVER")
    user: str = Field(env="POSTRES_USER")
    password: SecretStr = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="POSTGRES_HOST")
    port: int = Field(env="POSTGRES_PORT")
    database: str = Field(env="POSTGRES_DB")

    @property
    def dsn(self) -> str:
        return f"{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}"


class JWTSettings(Settings):
    secret: SecretStr = Field(env="JWT_SECRET")
    algorithm: str = Field(env="JWT_ALGORITHM")

    access_token_ttl: timedelta = Field(env="ACCESS_TOKEN_TTL")
    refresh_token_ttl: timedelta = Field(env="REFRESH_TOKEN_TTL")

    refresh_token_cookie: str = Field(env="REFRESH_TOKEN_COOKIE")


class PasswordSettings(Settings):
    encoding: str = Field(env="PASSWORD_ENCODING")
    rounds: int = Field(env="PASSWORD_SALT_ROUNDS")


class SignedRequestSettings(Settings):
    debug: bool = Field(env="DEBUG")
    secret: SecretStr = Field(env="SIGNATURE_SECRET")
    signature_header: str = Field(env="SIGNATURE_HEADER")
    encoding: str = Field(env="SIGNATURE_ENCODING")
    digest_mod: str = Field(env="SIGNATURE_DIGEST_MOD")
