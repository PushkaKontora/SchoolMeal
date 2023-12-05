import pytest

from app.users.application.services import SessionsService, UsersService
from app.users.domain.passwords import Password
from app.users.domain.session import CantRevokeAlreadyRevokedSession
from app.users.domain.tokens import AccessToken, RefreshToken
from app.users.domain.user import User
from tests.users.application.tokens import validate_tokens


async def test_refreshing(refresh_token: str, sessions_service: SessionsService):
    access_token, refresh_token = await sessions_service.refresh_session(refresh_token)

    validate_tokens(access_token, refresh_token, expected_user_id=refresh_token.user_id)


async def test_refreshing_after_logout(
    access_token: str, refresh_token: str, users_service: UsersService, sessions_service: SessionsService
):
    await users_service.logout(access_token)

    with pytest.raises(CantRevokeAlreadyRevokedSession):
        await sessions_service.refresh_session(refresh_token)


async def test_refreshing_using_revoked_token(refresh_token: str, sessions_service: SessionsService):
    await sessions_service.refresh_session(refresh_token)

    with pytest.raises(CantRevokeAlreadyRevokedSession):
        await sessions_service.refresh_session(refresh_token)


@pytest.fixture
async def tokens(parent: User, password: Password, users_service: UsersService) -> tuple[AccessToken, RefreshToken]:
    access: AccessToken | None = None
    refresh: RefreshToken | None = None

    for _ in range(3):
        access, refresh = await users_service.authenticate(parent.login.value, password.value)

    return access, refresh


@pytest.fixture
def access_token(tokens: tuple[AccessToken, RefreshToken], secret: str) -> str:
    return tokens[0].encode(secret)


@pytest.fixture
def refresh_token(tokens: tuple[AccessToken, RefreshToken], secret: str) -> str:
    return tokens[1].encode(secret)
