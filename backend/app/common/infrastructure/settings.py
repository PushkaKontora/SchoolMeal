from pydantic import BaseSettings, Field, SecretStr


class ServiceSettings(BaseSettings):
    show_swagger_ui: bool = Field(default=False, env="SHOW_SWAGGER_UI")


class DatabaseSettings(BaseSettings):
    driver: str = "postgresql+asyncpg"
    user: str = Field(default="postgres", env="DB_USER")
    password: str = Field(default="postgres", env="DB_PASSWORD")
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    database: str = Field(default="school_meal", env="DB_NAME")
    pool_size: int = 10

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class JWTSettings(BaseSettings):
    secret: SecretStr = Field(env="JWT_SECRET")


service = ServiceSettings()
database = DatabaseSettings()
jwt = JWTSettings()
