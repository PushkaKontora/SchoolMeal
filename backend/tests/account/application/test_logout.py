import pytest

from app.account.application.repositories import ICredentialsRepository, ISessionsRepository
from app.account.application.use_cases.jwt import authenticate, logout
from app.account.domain.login import Login
from app.account.domain.passwords import Password
from app.account.domain.tokens import AccessToken


async def test_logout(access: AccessToken, sessions_repository: ISessionsRepository):
    await logout(access, sessions_repository)

    revoked = await sessions_repository.get_all_by_credential_id_and_revoked(access.credential_id, revoked=True)
    assert len(revoked) == 1
    assert access.device_id == revoked[0].device_id


async def test_logout_using_old_access(access: AccessToken, sessions_repository: ISessionsRepository):
    for _ in range(2):
        await logout(access, sessions_repository)
        assert (
            len(await sessions_repository.get_all_by_credential_id_and_revoked(access.credential_id, revoked=True)) == 1
        )


@pytest.fixture
async def access(
    login: Login,
    password: Password,
    credentials_repository: ICredentialsRepository,
    sessions_repository: ISessionsRepository,
) -> AccessToken:
    access: AccessToken | None = None

    for _ in range(2):
        access, _ = await authenticate(login, password, credentials_repository, sessions_repository)

    return access
