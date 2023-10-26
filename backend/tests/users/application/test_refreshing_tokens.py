import pytest
from freezegun import freeze_time

from app.users.application.repositories import ISessionsRepository, IUsersRepository
from app.users.application.use_cases.jwt import authenticate, logout, refresh_tokens
from app.users.domain.passwords import Password
from app.users.domain.session import AlreadySessionRevokedError
from app.users.domain.tokens import AccessToken, RefreshToken
from app.users.domain.user import User
from tests.users.application.tokens import validate_tokens


@freeze_time()
async def test_refreshing(refresh_token: RefreshToken, sessions_repository: ISessionsRepository):
    access, refresh_token = await refresh_tokens(refresh_token, sessions_repository)

    validate_tokens(access, refresh_token, expected_user_id=refresh_token.user_id)

    assert len(await sessions_repository.get_all_by_user_id_and_revoked(refresh_token.user_id, revoked=True)) == 1


async def test_refreshing_after_logout(
    access: AccessToken, refresh_token: RefreshToken, sessions_repository: ISessionsRepository
):
    await logout(access, sessions_repository)

    with pytest.raises(AlreadySessionRevokedError):
        await refresh_tokens(refresh_token, sessions_repository)

    assert len(await sessions_repository.get_all_by_user_id_and_revoked(refresh_token.user_id, revoked=False)) == 0


async def test_refreshing_using_revoked_token(refresh_token: RefreshToken, sessions_repository: ISessionsRepository):
    await refresh_tokens(refresh_token, sessions_repository)

    with pytest.raises(AlreadySessionRevokedError):
        await refresh_tokens(refresh_token, sessions_repository)

    assert len(await sessions_repository.get_all_by_user_id_and_revoked(refresh_token.user_id, revoked=False)) == 0


@pytest.fixture
async def tokens(
    parent: User,
    password: Password,
    users_repository: IUsersRepository,
    sessions_repository: ISessionsRepository,
) -> tuple[AccessToken, RefreshToken]:
    access: AccessToken | None = None
    refresh: RefreshToken | None = None

    for _ in range(3):
        access, refresh = await authenticate(parent.login, password, users_repository, sessions_repository)

    return access, refresh


@pytest.fixture
def access(tokens: tuple[AccessToken, RefreshToken]) -> AccessToken:
    return tokens[0]


@pytest.fixture
def refresh_token(tokens: tuple[AccessToken, RefreshToken]) -> RefreshToken:
    return tokens[1]
