from pydantic import BaseSettings, Field


class JWTConfig(BaseSettings):
    secret: str = Field(env="JWT_SECRET")
