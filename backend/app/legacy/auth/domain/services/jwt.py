from datetime import datetime, timedelta

from dependency_injector.wiring import Provide
from jwt import PyJWTError, decode, encode

from app.config import JWTSettings
from app.legacy.auth.domain.entities import JWTPayload, JWTTokensOut, TokenType
from app.legacy.auth.domain.errors import InvalidTokenSignatureError, TokenExpirationError
from app.legacy.container import AppContainer
from app.legacy.users.db.user.model import Role


def decode_access_token(token: str) -> JWTPayload:
    payload = try_decode(token)

    if not payload or payload.type != TokenType.ACCESS:
        raise InvalidTokenSignatureError

    if is_token_expired_in(payload.expires_in):
        raise TokenExpirationError

    return payload


def generate_tokens(user_id: int, role: Role) -> JWTTokensOut:
    tokens = JWTTokensOut(
        access_token=generate_token(TokenType.ACCESS, user_id, role),
        refresh_token=generate_token(TokenType.REFRESH, user_id, role),
    )

    return tokens


def generate_token(
    token_type: TokenType, user_id: int, role: Role, settings: JWTSettings = Provide[AppContainer.jwt_settings]
) -> str:
    ttl = _get_token_ttl(token_type, settings)

    payload = JWTPayload(
        type=token_type, user_id=user_id, role=role, expires_in=int((datetime.utcnow() + ttl).timestamp())
    )

    return encode(payload.dict(), settings.secret.get_secret_value(), settings.algorithm)


def try_decode(token: str, settings: JWTSettings = Provide[AppContainer.jwt_settings]) -> JWTPayload | None:
    try:
        payload = decode(token, key=settings.secret.get_secret_value(), algorithms=[settings.algorithm])
    except PyJWTError:
        return None

    return JWTPayload(**payload)


def is_token_expired(
    created_at: datetime, token_type: TokenType, settings: JWTSettings = Provide[AppContainer.jwt_settings]
) -> bool:
    return datetime.utcnow() >= created_at + _get_token_ttl(token_type, settings)


def is_token_expired_in(timestamp: float) -> bool:
    return datetime.utcnow().timestamp() >= timestamp


def _get_token_ttl(token_type: TokenType, settings: JWTSettings) -> timedelta:
    match token_type:
        case TokenType.ACCESS:
            return settings.access_lifetime

        case TokenType.REFRESH:
            return settings.refresh_lifetime

    raise UnknownTokenTypeException


class UnknownTokenTypeException(Exception):
    pass
