from pydantic import BaseSettings, Field


class JWTSettings(BaseSettings):
    secret: str = Field(env="JWT_SECRET")
