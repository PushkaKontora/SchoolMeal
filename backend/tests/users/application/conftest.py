import pytest

from app.users.application.services import UsersService
from app.users.application.unit_of_work import UsersContext
from app.users.domain.email import Email
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import Password
from app.users.domain.phone import Phone
from app.users.domain.user import User
from tests.unit_of_work import LocalUnitOfWork
from tests.users.application.repositories import LocalSessionsRepository, LocalUsersRepository


@pytest.fixture(scope="session")
def parent(password: Password) -> User:
    return User.create_parent(
        first_name=FirstName("Лима"),
        last_name=LastName("Дыков"),
        phone=Phone("+7 (800) 555-35-35"),
        email=Email("serious_dim@urfu.me"),
        password=password.as_strict(),
    )


@pytest.fixture(scope="session")
def password() -> Password:
    return Password("P@ssw0rd1234")


@pytest.fixture
def users_service(parent: User, secret: str) -> UsersService:
    return UsersService(
        unit_of_work=LocalUnitOfWork(
            lambda: UsersContext(
                users=LocalUsersRepository([parent]),
                sessions=LocalSessionsRepository(),
            )
        ),
        secret=secret,
    )


@pytest.fixture
def secret() -> str:
    return "a" * 10
