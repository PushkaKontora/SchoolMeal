from os.path import join
from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn


BASE_DIR = Path(__file__).resolve().parent.parent

_DOT_ENV = join(BASE_DIR, ".env")


class DatabaseSettings(BaseSettings):
    dsn: PostgresDsn = Field(env="POSTGRES_DSN")

    class Config:
        env_file = _DOT_ENV
