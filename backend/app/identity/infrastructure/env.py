from pydantic import BaseSettings, Field


class AuthConfig(BaseSettings):
    secret: str = Field(env="JWT_SECRET")
