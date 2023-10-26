import pytest

from app.users.application.repositories import ISessionsRepository, IUsersRepository
from app.users.application.use_cases.jwt import authenticate
from app.users.application.use_cases.user import get_user_by_access_token
from app.users.domain.passwords import Password
from app.users.domain.tokens import AccessToken
from app.users.domain.user import User


async def test_getting_user_by_access_token(
    parent: User, access_token: AccessToken, users_repository: IUsersRepository
):
    user = await get_user_by_access_token(access_token=access_token, users_repository=users_repository)

    assert user == parent


@pytest.fixture
async def access_token(
    parent: User,
    password: Password,
    users_repository: IUsersRepository,
    sessions_repository: ISessionsRepository,
) -> AccessToken:
    return (
        await authenticate(
            login=parent.login,
            password=password,
            users_repository=users_repository,
            sessions_repository=sessions_repository,
        )
    )[0]
