from pydantic import BaseSettings, Field, SecretStr


class JWTSettings(BaseSettings):
    secret: str = Field(env="JWT_SECRET")
