import pytest

from app.users.application.repositories import ISessionsRepository, IUsersRepository
from app.users.application.use_cases.jwt import authenticate, logout
from app.users.domain.passwords import Password
from app.users.domain.tokens import AccessToken
from app.users.domain.user import User


async def test_logout(access: AccessToken, sessions_repository: ISessionsRepository):
    await logout(access, sessions_repository)

    revoked = await sessions_repository.get_all_by_user_id_and_revoked(access.user_id, revoked=True)
    assert len(revoked) == 1
    assert access.device_id == revoked[0].device_id


async def test_logout_using_old_access(access: AccessToken, sessions_repository: ISessionsRepository):
    for _ in range(2):
        await logout(access, sessions_repository)
        assert len(await sessions_repository.get_all_by_user_id_and_revoked(access.user_id, revoked=True)) == 1


@pytest.fixture
async def access(
    parent: User,
    password: Password,
    users_repository: IUsersRepository,
    sessions_repository: ISessionsRepository,
) -> AccessToken:
    access: AccessToken | None = None

    for _ in range(2):
        access, _ = await authenticate(parent.login, password, users_repository, sessions_repository)

    return access
