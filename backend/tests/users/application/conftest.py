import pytest

from app.users.application.repositories import ISessionsRepository, IUsersRepository
from app.users.domain.email import Email
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import Password
from app.users.domain.phone import Phone
from app.users.domain.user import User
from tests.users.application.repositories import LocalSessionsRepository, LocalUsersRepository


@pytest.fixture(scope="session")
def parent(password: Password) -> User:
    return User.create_parent(
        first_name=FirstName("Лима"),
        last_name=LastName("Дыков"),
        phone=Phone("+7 (800) 555-35-35"),
        email=Email("serious_dim@urfu.me"),
        password=password,
    )


@pytest.fixture(scope="session")
def password() -> Password:
    return Password("P@ssw0rd1234")


@pytest.fixture
def users_repository(parent: User) -> IUsersRepository:
    return LocalUsersRepository(users=[parent])


@pytest.fixture
def sessions_repository() -> ISessionsRepository:
    return LocalSessionsRepository()
