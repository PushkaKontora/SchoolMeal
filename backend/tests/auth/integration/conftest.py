from datetime import datetime, timedelta
from enum import Enum

import jwt
import pytest
from bcrypt import gensalt, hashpw
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import now

from app.auth.db.issued_token.model import IssuedToken
from app.auth.db.password.model import Password
from app.config import JWTSettings
from app.users.db.user.model import Role, User
from tests.utils import get_set_cookies


AUTH_PREFIX = "/auth"

OLD_PASSWORD, ACTUAL_PASSWORD = ["old_pass", "actual_pass"]
LOGIN = "metkij_strelok"
OLD_HASHED_PASSWORD, ACTUAL_HASHED_PASSWORD = [
    hashpw(p.encode("utf-8"), gensalt()) for p in [OLD_PASSWORD, ACTUAL_PASSWORD]
]


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


@pytest.fixture
async def user(session: AsyncSession) -> User:
    user = User(
        last_name="Dykov",
        first_name="Lima",
        login=LOGIN,
        role=Role.PARENT,
        phone="+78005553535",
        email="email@email.com",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    old_password, new_password = [
        Password(user_id=user.id, value=p, created_at=now() + delta)
        for p, delta in {OLD_HASHED_PASSWORD: timedelta(0), ACTUAL_HASHED_PASSWORD: timedelta(days=10)}.items()
    ]

    session.add(old_password)
    session.add(new_password)
    await session.commit()

    return user


@pytest.fixture
async def another_user(session: AsyncSession) -> User:
    user = User(
        last_name="Yerov",
        first_name="Pura",
        login="<XoXo>",
        role=Role.PARENT,
        phone="+79617639012",
        email="123@123.com",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture
async def user_refresh_token(session: AsyncSession, user: User, auth_settings: JWTSettings) -> IssuedToken:
    return await create_refresh_token(session, user.id, user.role, auth_settings)


@pytest.fixture
async def another_user_refresh_token(
    session: AsyncSession, another_user: User, auth_settings: JWTSettings
) -> IssuedToken:
    return await create_refresh_token(session, another_user.id, another_user.role, auth_settings)


async def create_refresh_token(
    session: AsyncSession,
    user_id: int,
    role: Role,
    auth_settings: JWTSettings,
    revoked: bool = False,
    created_at: datetime = None,
) -> IssuedToken:
    payload = get_expected_payload(TokenType.REFRESH, user_id, role, auth_settings.refresh_token_ttl)
    value = generate_token(payload, auth_settings.secret.get_secret_value(), auth_settings.algorithm)

    token = IssuedToken(user_id=user_id, value=value, revoked=revoked)
    token.created_at = created_at or token.created_at
    session.add(token)
    await session.commit()
    await session.refresh(token)

    return token


def create_access_token(user_id: int, role: Role, jwt_settings: JWTSettings) -> str:
    payload = get_expected_payload(TokenType.ACCESS, user_id, role, jwt_settings.access_token_ttl)
    return generate_token(payload, jwt_settings.secret.get_secret_value(), jwt_settings.algorithm)


def generate_token(payload: dict, secret: str, algorithm: str) -> str:
    return jwt.encode(payload, secret, algorithm)


def get_expected_payload(token_type: TokenType, user_id: int, role: Role, ttl: timedelta) -> dict:
    return {
        "type": token_type.value,
        "user_id": user_id,
        "role": role.value,
        "expires_in": int((datetime.utcnow() + ttl).timestamp()),
    }


def assert_payload_contains_valid_access_token(
    response: Response, user: User, ttl: timedelta, field_name: str = "accessToken"
):
    body: dict = response.json()
    assert list(body.keys()) == [field_name]
    validate_token(body[field_name], TokenType.ACCESS, user.id, user.role, ttl)


def assert_response_contains_cookie_with_refresh_token(
    response: Response, user: User, ttl: timedelta, cookie_name: str = "refresh_token"
):
    cookies = get_set_cookies(response.headers)

    assert cookie_name in cookies
    validate_token(cookies[cookie_name], TokenType.REFRESH, user.id, user.role, ttl)


def validate_token(
    token: str, expected_type: TokenType, expected_user_id, expected_user_role: Role, expected_ttl: timedelta
):
    payload = jwt.decode(token, options={"verify_signature": False})
    assert payload == get_expected_payload(expected_type, expected_user_id, expected_user_role, expected_ttl)
