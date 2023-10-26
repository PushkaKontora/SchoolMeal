import pytest

from app.users.domain.email import Email
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import Password
from app.users.domain.phone import Phone
from app.users.domain.role import Role
from app.users.domain.user import PasswordIsNotVerified, User


def test_creating_parent(last_name: LastName, first_name: FirstName, phone: Phone, email: Email, password: Password):
    parent = User.create_parent(first_name, last_name, phone, email, password.as_strict())

    assert parent.last_name == last_name
    assert parent.first_name == first_name
    assert parent.login.value == phone.value
    assert parent.phone == phone
    assert parent.email == email
    assert parent.role == Role.PARENT


def test_authentication(user: User, password: Password):
    authenticated_user = user.authenticate(password)

    assert authenticated_user == user


def test_authentication_using_incorrect_password(user: User):
    with pytest.raises(PasswordIsNotVerified):
        user.authenticate(password=Password("P@ssw0ordIncorrect1234"))


@pytest.fixture
def user(last_name: LastName, first_name: FirstName, phone: Phone, email: Email, password: Password) -> User:
    return User.create_parent(first_name, last_name, phone, email, password.as_strict())


@pytest.fixture
def last_name() -> LastName:
    return LastName("Лыков")


@pytest.fixture
def first_name() -> FirstName:
    return FirstName("Димон")


@pytest.fixture
def phone() -> Phone:
    return Phone("+7 (800) 555-35-35")


@pytest.fixture
def email() -> Email:
    return Email("serious_dim@google.com")


@pytest.fixture
def password() -> Password:
    return Password("P@ssw0rd1234")
