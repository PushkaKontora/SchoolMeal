from datetime import datetime
from enum import Enum

from app.entities import BaseEntity


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class Password(BaseEntity):
    id: int
    user_id: int
    value: bytes
    created_at: datetime


class LoginSchema(BaseEntity):
    login: str
    password: str


class AuthenticationOut(BaseEntity):
    access_token: str


class JWTTokens(AuthenticationOut):
    refresh_token: str
