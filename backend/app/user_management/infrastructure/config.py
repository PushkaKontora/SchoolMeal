from pydantic import BaseSettings, Field


class Config(BaseSettings):
    domain: str = Field(env="DOMAIN")
    jwt_secret: str = Field(env="JWT_SECRET")
