from datetime import datetime, timedelta
from enum import IntEnum, auto

import freezegun
import pytest
from httpx import AsyncClient, Cookies, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.db.models import IssuedToken
from app.config import JWTSettings
from app.users.db.models import User
from tests.auth.conftest import (
    AUTH_PREFIX,
    TokenType,
    assert_payload_contains_valid_access_token,
    assert_response_contains_cookie_with_refresh_token,
    create_refresh_token,
    generate_token,
    get_expected_payload,
)
from tests.responses import error


pytestmark = [pytest.mark.integration]

URL = AUTH_PREFIX + "/refresh-tokens"


class TokenState(IntEnum):
    REVOKED = auto()
    EXPIRED = auto()


async def refresh(client: AsyncClient, auth_settings: JWTSettings, refresh_token: str = None) -> Response:
    cookies = Cookies()

    if refresh_token is not None:
        cookies.set(auth_settings.refresh_token_cookie, refresh_token)

    return await client.post(URL, cookies=cookies)


@freezegun.freeze_time()
async def test_refresh(
    client: AsyncClient,
    session: AsyncSession,
    user: User,
    user_refresh_token: IssuedToken,
    another_user_refresh_token: IssuedToken,
    auth_settings: JWTSettings,
):
    with freezegun.freeze_time(datetime.now() + timedelta(seconds=1)):
        refresh_token = await create_refresh_token(session, user.id, user.role, auth_settings)

    with freezegun.freeze_time(datetime.now() + timedelta(seconds=2)):
        response = await refresh(client, auth_settings, refresh_token.value)

        assert response.status_code == 200
        assert_payload_contains_valid_access_token(response, user, auth_settings.access_token_ttl)
        assert_response_contains_cookie_with_refresh_token(response, user, auth_settings.refresh_token_ttl)

        await session.refresh(refresh_token, ["revoked"])
        await session.refresh(user_refresh_token, ["revoked"])
        await session.refresh(another_user_refresh_token, ["revoked"])

        assert refresh_token.revoked is True
        assert user_refresh_token.revoked is False
        assert another_user_refresh_token.revoked is False


@pytest.mark.parametrize(
    ["delta", "revoked", "state"],
    [
        [timedelta(0), False, TokenState.EXPIRED],
        [timedelta(seconds=1), False, TokenState.EXPIRED],
        [-timedelta(seconds=1), True, TokenState.REVOKED],
        [timedelta(0), True, TokenState.REVOKED],
    ],
    ids=[
        "a token expired at the time of the specified value",
        "a token expired a second ago",
        "a token is revoked but has not expired",
        "a token expired and is revoked",
    ],
)
@freezegun.freeze_time()
async def test_refresh_with_expired_or_revoked_token(
    client: AsyncClient,
    session: AsyncSession,
    user: User,
    user_refresh_token: IssuedToken,
    another_user_refresh_token: IssuedToken,
    auth_settings: JWTSettings,
    state: TokenState,
    delta: timedelta,
    revoked: bool,
):
    with freezegun.freeze_time(datetime.utcnow() - auth_settings.refresh_token_ttl - delta):
        refresh_token = await create_refresh_token(
            session, user.id, user.role, auth_settings, revoked=revoked, created_at=datetime.utcnow()
        )

    response = await refresh(client, auth_settings, refresh_token.value)

    assert response.status_code == 400

    await session.refresh(refresh_token, ["revoked"])
    await session.refresh(user_refresh_token, ["revoked"])
    await session.refresh(another_user_refresh_token, ["revoked"])

    match state:
        case TokenState.EXPIRED:
            assert response.json() == error("TokenExpirationException", "The token expired")

            assert refresh_token.revoked is True
            assert user_refresh_token.revoked is False
            assert another_user_refresh_token.revoked is False

        case TokenState.REVOKED:
            assert response.json() == error("RefreshWithRevokedTokenException", "The token is already revoked")

            assert refresh_token.revoked is True
            assert user_refresh_token.revoked is True
            assert another_user_refresh_token.revoked is False


async def test_refresh_with_damaged_signature(
    client: AsyncClient, session: AsyncSession, user: User, auth_settings: JWTSettings, secret: str = "bad secret"
):
    payload = get_expected_payload(TokenType.REFRESH, user.id, user.role, auth_settings.refresh_token_ttl)
    refresh_token = generate_token(payload, secret, auth_settings.algorithm)

    response = await refresh(client, auth_settings, refresh_token)

    assert response.status_code == 400
    assert response.json() == error("InvalidTokenSignatureException", "The token's signature was destroyed")

    await assert_db_has_not_been_changed(session)


async def test_refresh_with_empty_cookie(
    client: AsyncClient,
    session: AsyncSession,
    user_refresh_token: IssuedToken,
    another_user_refresh_token: IssuedToken,
    auth_settings: JWTSettings,
):
    response = await refresh(client, auth_settings, refresh_token=None)

    assert response.status_code == 400
    assert response.json() == error("NotFoundRefreshCookieException", "A refresh token is not found in cookies")

    await assert_db_has_not_been_changed(session)


async def test_refresh_with_unknown_refresh_token(
    client: AsyncClient, user: User, session: AsyncSession, auth_settings: JWTSettings
):
    unknown_token = await create_refresh_token(session, user.id, user.role, auth_settings)
    await session.delete(unknown_token)
    await session.commit()

    response = await refresh(client, auth_settings, unknown_token.value)

    assert response.status_code == 400
    assert response.json() == error(
        "NotFoundRefreshTokenException", "The token was not created or was deleted by the service"
    )

    await assert_db_has_not_been_changed(session)


async def assert_db_has_not_been_changed(session: AsyncSession):
    query = select(IssuedToken).with_only_columns(func.count()).where(IssuedToken.revoked is True)

    assert (await session.scalar(query)) == 0
