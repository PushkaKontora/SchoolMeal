from datetime import datetime
from enum import Enum

from app.entities import BaseEntity


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class Password(BaseEntity):
    id: int
    user_id: int
    value: bytes
    created_at: datetime


class IssuedToken(BaseEntity):
    value: str
    user_id: int
    revoked: bool
    created_at: datetime


class LoginSchema(BaseEntity):
    login: str
    password: str


class AccessTokenOut(BaseEntity):
    access_token: str


class JWTTokens(AccessTokenOut):
    refresh_token: str
