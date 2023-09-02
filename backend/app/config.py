from abc import ABC
from datetime import timedelta
from enum import Enum
from os.path import join
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import AnyHttpUrl, BaseSettings, Field


BASE_DIR = Path(__file__).resolve().parent.parent


class Environment(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class Settings(BaseSettings, ABC):
    class Config:
        env_file = join(BASE_DIR, ".env")


class AppSettings(Settings):
    environment: Environment = Field(env="ENV")
    timezone_name: str = Field(env="TZ")
    docs_url: str = "/docs"

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.timezone_name)


class HeadersSettings(Settings):
    real_ip_header: str = "X-Real-IP"


class DatabaseSettings(Settings):
    driver: str = Field(env="POSTGRES_DRIVER")
    user: str = Field(env="POSTGRES_USER")
    password: str = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="POSTGRES_HOST")
    port: int = Field(env="POSTGRES_PORT")
    database: str = Field(env="POSTGRES_DB")
    pool_size: int = Field(env="POSTGRES_POOL_SIZE")

    @property
    def dsn(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class JWTSettings(Settings):
    algorithm: str = "HS256"
    secret: str = Field(env="JWT_SECRET")
    access_lifetime: timedelta = Field(env="JWT_ACCESS_LIFETIME")
    refresh_lifetime: timedelta = Field(env="JWT_REFRESH_LIFETIME")
    refresh_cookie: str = "rf_tk"


class PasswordSettings(Settings):
    encoding: str = "utf-8"
    rounds: int = 12


class CORSSettings(Settings):
    origins: tuple[str] = ("*",)
    allow_credentials: bool = True
    methods: tuple[str] = ("*",)
    headers: tuple[str] = ("*",)


class S3StorageSettings(Settings):
    access_key: str = Field(env="AWS_ACCESS_KEY")
    secret_key: str = Field(env="AWS_SECRET_KEY")
    endpoint: AnyHttpUrl = Field(env="AWS_ENDPOINT_URL")
    bucket_name: str = Field(env="AWS_BUCKET_NAME")
    resource_url_lifetime: timedelta = Field(env="AWS_RESOURCE_URL_LIFETIME")


base = AppSettings()
headers = HeadersSettings()
cors = CORSSettings()
database = DatabaseSettings()
jwt = JWTSettings()
