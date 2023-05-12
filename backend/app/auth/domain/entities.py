from enum import Enum

from app.users.db.user.model import Role
from app.utils.entity import Entity


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class JWTPayload(Entity):
    type: TokenType
    user_id: int
    role: Role
    expires_in: int


class CredentialsIn(Entity):
    login: str
    password: str


class AccessTokenOut(Entity):
    access_token: str


class JWTTokensOut(AccessTokenOut):
    refresh_token: str
