import pytest
from freezegun import freeze_time

from app.account.application.repositories import ICredentialsRepository, ISessionsRepository
from app.account.application.use_cases.jwt import authenticate, logout, refresh_tokens
from app.account.domain.login import Login
from app.account.domain.passwords import Password
from app.account.domain.session import AlreadySessionRevokedError
from app.account.domain.tokens import AccessToken, RefreshToken
from tests.account.application.tokens import validate_tokens


@freeze_time()
async def test_refreshing(refresh: RefreshToken, sessions_repository: ISessionsRepository):
    access, refresh = await refresh_tokens(refresh, sessions_repository)

    validate_tokens(access, refresh, expected_credential_id=refresh.credential_id)

    assert len(await sessions_repository.get_all_by_credential_id_and_revoked(refresh.credential_id, revoked=True)) == 1


async def test_refreshing_after_logout(
    access: AccessToken, refresh: RefreshToken, sessions_repository: ISessionsRepository
):
    await logout(access, sessions_repository)

    with pytest.raises(AlreadySessionRevokedError):
        await refresh_tokens(refresh, sessions_repository)

    assert (
        len(await sessions_repository.get_all_by_credential_id_and_revoked(refresh.credential_id, revoked=False)) == 0
    )


async def test_refreshing_using_revoked_token(refresh: RefreshToken, sessions_repository: ISessionsRepository):
    await refresh_tokens(refresh, sessions_repository)

    with pytest.raises(AlreadySessionRevokedError):
        await refresh_tokens(refresh, sessions_repository)

    assert (
        len(await sessions_repository.get_all_by_credential_id_and_revoked(refresh.credential_id, revoked=False)) == 0
    )


@pytest.fixture
async def tokens(
    login: Login,
    password: Password,
    credentials_repository: ICredentialsRepository,
    sessions_repository: ISessionsRepository,
) -> tuple[AccessToken, RefreshToken]:
    access: AccessToken | None = None
    refresh: RefreshToken | None = None

    for _ in range(3):
        access, refresh = await authenticate(login, password, credentials_repository, sessions_repository)

    return access, refresh


@pytest.fixture
def access(tokens: tuple[AccessToken, RefreshToken]) -> AccessToken:
    return tokens[0]


@pytest.fixture
def refresh(tokens: tuple[AccessToken, RefreshToken]) -> RefreshToken:
    return tokens[1]
