import pytest

from app.account.domain.email import Email
from app.account.domain.names import FirstName, LastName
from app.account.domain.passwords import Password
from app.account.domain.phone import Phone
from app.account.domain.role import Role
from app.account.domain.user import User


def test_creating_parent(last_name: LastName, first_name: FirstName, phone: Phone, email: Email, password: Password):
    parent = User.create_parent(first_name, last_name, phone, email, password)

    assert parent.last_name == last_name
    assert parent.first_name == first_name
    assert parent.phone == phone
    assert parent.email == email
    assert parent.role == Role.PARENT

    credential = parent.credential
    assert credential.login.value == phone.value
    assert credential.password.verify(password) is True


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
