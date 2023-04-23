from enum import Enum

from app.base_entity import BaseEntity
from app.users.db.models import Role


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTPayload(BaseEntity):
    type: TokenType
    user_id: int
    role: Role
    expires_in: int


class LoginSchema(BaseEntity):
    login: str
    password: str


class AccessTokenOut(BaseEntity):
    access_token: str


class JWTTokens(AccessTokenOut):
    refresh_token: str
