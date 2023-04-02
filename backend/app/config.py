from os.path import join
from pathlib import Path

from pydantic import BaseSettings, Field


BASE_DIR = Path(__file__).resolve().parent.parent
DOT_ENV_PATH = join(BASE_DIR, ".env")


class DatabaseSettings(BaseSettings):
    driver: str = Field(env="DB_DRIVER")
    name: str = Field(env="DB_NAME")
    user: str = Field(env="DB_USER")
    password: str = Field(env="DB_PASSWORD")
    host: str = Field(env="DB_HOST")
    port: int = Field(env="DB_PORT")

    @property
    def dsn(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


database = DatabaseSettings(_env_file=DOT_ENV_PATH)
