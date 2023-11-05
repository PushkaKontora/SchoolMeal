import pytest

from app.account.application.repositories import ICredentialsRepository, ISessionsRepository, IUsersRepository
from app.account.application.use_cases.jwt import authenticate
from app.account.application.use_cases.user import get_user_by_access
from app.account.domain.passwords import Password
from app.account.domain.tokens import AccessToken
from app.account.domain.user import User


async def test_getting_user_by_access_token(
    registered_parent: User, access_token: AccessToken, users_repository: IUsersRepository
):
    user = await get_user_by_access(access=access_token, users_repository=users_repository)

    assert user == registered_parent


@pytest.fixture
async def access_token(
    registered_parent: User,
    password: Password,
    credentials_repository: ICredentialsRepository,
    sessions_repository: ISessionsRepository,
) -> AccessToken:
    return (
        await authenticate(
            login=registered_parent.credential.login,
            password=password,
            credentials_repository=credentials_repository,
            sessions_repository=sessions_repository,
        )
    )[0]
