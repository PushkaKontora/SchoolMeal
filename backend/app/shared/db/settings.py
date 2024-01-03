from pydantic import BaseSettings, Field


class DatabaseSettings(BaseSettings):
    driver: str = "postgresql+asyncpg"
    user: str = Field(default="postgres", env="DB_USER")
    password: str = Field(default="postgres", env="DB_PASSWORD")
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    database: str = Field(default="school_meal", env="DB_NAME")

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class AlchemySettings(BaseSettings):
    echo: bool = Field(env="ALCHEMY_ECHO", default=False)
    pool_size: int = Field(env="ALCHEMY_POOL_SIZE", default=10)
