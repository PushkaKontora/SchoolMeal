from datetime import datetime, timedelta

import freezegun
import pytest
from httpx import AsyncClient, Cookies, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.db.issued_token.model import IssuedToken
from app.config import JWTSettings
from app.users.db.user.model import User
from tests.auth.integration.conftest import AUTH_PREFIX, create_refresh_token
from tests.responses import error


pytestmark = [pytest.mark.integration]


URL = AUTH_PREFIX + "/logout"


async def logout(client: AsyncClient, cookies: Cookies) -> Response:
    return await client.post(URL, cookies=cookies)


async def test_logout(
    client: AsyncClient,
    session: AsyncSession,
    user: User,
    user_refresh_token: IssuedToken,
    another_user_refresh_token: IssuedToken,
    auth_settings: JWTSettings,
):
    with freezegun.freeze_time(datetime.now() + timedelta(days=10)):
        another_token = await create_refresh_token(session, user.id, user.role, auth_settings)

    cookies = Cookies()
    cookies.set(auth_settings.refresh_token_cookie, user_refresh_token.value)
    response = await logout(client, cookies)

    assert response.status_code == 200

    await session.refresh(user_refresh_token, ["revoked"])
    await session.refresh(another_token, ["revoked"])
    assert user_refresh_token.revoked is True
    assert another_token.revoked is False

    await session.refresh(another_user_refresh_token, ["revoked"])
    assert another_user_refresh_token.revoked is False


async def test_request_that_does_not_contain_cookie(
    client: AsyncClient, session: AsyncSession, user_refresh_token: IssuedToken
):
    response = await logout(client, Cookies())

    assert response.status_code == 400
    assert response.json() == error("NotFoundRefreshCookieException", "A refresh token is not found in cookies")

    await session.refresh(user_refresh_token, ["revoked"])
    assert user_refresh_token.revoked is False


@freezegun.freeze_time()
async def test_request_that_contains_damaged_token(
    client: AsyncClient, session: AsyncSession, user: User, user_refresh_token: IssuedToken, auth_settings: JWTSettings
):
    with freezegun.freeze_time(datetime.utcnow() + timedelta(seconds=1)):
        token = await create_refresh_token(session, user.id, user.role, auth_settings)

    cookies = Cookies()
    cookies.set(auth_settings.refresh_token_cookie, token.value[:-2])
    response = await logout(client, cookies)

    assert response.status_code == 400
    assert response.json() == error("InvalidTokenSignatureException", "The token's signature was destroyed")

    await session.refresh(user_refresh_token, ["revoked"])
    await session.refresh(token, ["revoked"])
    assert user_refresh_token.revoked is False
    assert token.revoked is False
