from uuid import UUID

import pytest

from app.account.application.repositories import ICredentialsRepository, ISessionsRepository, IUsersRepository
from app.account.domain.email import Email
from app.account.domain.login import Login
from app.account.domain.names import FirstName, LastName
from app.account.domain.passwords import HashedPassword, Password
from app.account.domain.phone import Phone
from app.account.domain.user import User
from tests.account.application.repositories import (
    LocalCredentialsRepository,
    LocalSessionsRepository,
    LocalUsersRepository,
)


@pytest.fixture(scope="session")
def registered_parent() -> User:
    return User.create_parent(
        first_name=FirstName("Лима"),
        last_name=LastName("Дыков"),
        phone=Phone("+7 (800) 555-35-35"),
        email=Email("serious_dim@urfu.me"),
        password=Password("P@ssw0rd1234"),
    )


@pytest.fixture(scope="session")
def credential_id(registered_parent: User) -> UUID:
    return registered_parent.credential.id


@pytest.fixture(scope="session")
def login(registered_parent: User) -> Login:
    return registered_parent.credential.login


@pytest.fixture(scope="session")
def password(registered_parent: User) -> Password:
    return Password("P@ssw0rd1234")


@pytest.fixture(scope="session")
def hashed_password(password: Password) -> HashedPassword:
    return password.hash()


@pytest.fixture
def credentials_repository(registered_parent: User) -> ICredentialsRepository:
    return LocalCredentialsRepository(credentials=[registered_parent.credential])


@pytest.fixture
def users_repository(registered_parent: User) -> IUsersRepository:
    return LocalUsersRepository(users=[registered_parent])


@pytest.fixture
def sessions_repository() -> ISessionsRepository:
    return LocalSessionsRepository()
