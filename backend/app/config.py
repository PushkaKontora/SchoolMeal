from abc import ABC
from datetime import time, timedelta
from enum import Enum
from os.path import join
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import AnyHttpUrl, BaseSettings, Field, SecretStr


BASE_DIR = Path(__file__).resolve().parent.parent


class Environment(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings, ABC):
    class Config:
        env_file = join(BASE_DIR, ".env")


class AppSettings(Settings):
    environment: Environment = Field(env="ENV")
    debug: bool = Field(env="DEBUG")
    docs_url: str = Field(env="DOCS_URL")


class DatetimeSettings(Settings):
    timezone_name: str = Field(env="TZ")

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.timezone_name)


class MealRequestSettings(Settings):
    creating_time: time = Field(env="MEAL_REQUEST_CREATING_TIME")
    last_updating_time: time = Field(env="MEAL_REQUEST_LAST_UPDATING_TIME")


class DatabaseSettings(Settings):
    driver: str = Field(env="POSTGRES_DRIVER")
    user: str = Field(env="POSTGRES_USER")
    password: SecretStr = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="POSTGRES_HOST")
    port: int = Field(env="POSTGRES_PORT")
    database: str = Field(env="POSTGRES_DB")
    pool_size: int = Field(env="POSTGRES_POOL_SIZE")

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


class RequestSignatureSettings(Settings):
    secret: SecretStr = Field(env="SIGNATURE_SECRET")
    signature_header: str = Field(env="SIGNATURE_HEADER")
    encoding: str = Field(env="SIGNATURE_ENCODING")
    digest_mod: str = Field(env="SIGNATURE_DIGEST_MOD")


class CORSSettings(Settings):
    origins: list[str] = Field(env="CORS_ALLOW_ORIGINS")
    allow_credentials: bool = Field(env="CORS_ALLOW_CREDENTIALS")
    methods: list[str] = Field(env="CORS_ALLOW_METHODS")
    headers: list[str] = Field(env="CORS_ALLOW_HEADERS")


class S3StorageSettings(Settings):
    access_key: str = Field(env="AWS_ACCESS_KEY")
    secret_key: str = Field(env="AWS_SECRET_KEY")
    endpoint: AnyHttpUrl = Field(env="AWS_ENDPOINT_URL")
    bucket_name: str = Field(env="AWS_BUCKET_NAME")
    presigned_url_ttl: timedelta = Field(env="AWS_PRESIGNED_URL_TTL")


app = AppSettings()
cors = CORSSettings()
datetime = DatetimeSettings()
database = DatabaseSettings()
jwt = JWTSettings()
