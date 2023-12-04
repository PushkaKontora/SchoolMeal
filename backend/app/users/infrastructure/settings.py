from pydantic import BaseSettings, Field, SecretStr


class JWTSettings(BaseSettings):
    secret: SecretStr = Field(env="JWT_SECRET")
