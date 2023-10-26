import pytest

from app.account.application.repositories import IUsersRepository
from app.account.application.use_cases.registration import AlreadyRegisteredPhoneError, register_parent
from app.account.domain.email import Email
from app.account.domain.names import FirstName, LastName
from app.account.domain.passwords import Password
from app.account.domain.phone import Phone
from app.account.domain.user import User


async def test_registration_parent(
    first_name: FirstName,
    last_name: LastName,
    phone: Phone,
    email: Email,
    password: Password,
    users_repository: IUsersRepository,
):
    user = await register_parent(first_name, last_name, phone, email, password, users_repository)

    assert user.last_name == last_name
    assert user.first_name == first_name
    assert user.phone == phone
    assert user.email == email

    credential = user.credential
    assert credential.login.value == phone.value
    assert credential.password.verify(password) is True


async def test_registration_parent_using_not_unique_phone(
    registered_parent: User,
    first_name: FirstName,
    last_name: LastName,
    email: Email,
    password: Password,
    users_repository: IUsersRepository,
):
    with pytest.raises(AlreadyRegisteredPhoneError) as error_info:
        await register_parent(
            first_name=first_name,
            last_name=last_name,
            phone=registered_parent.phone,
            email=email,
            password=password,
            users_repository=users_repository,
        )

    assert str(error_info.value) == "Телефон уже зарегистрирован"


@pytest.fixture
def last_name() -> LastName:
    return LastName("Самков")


@pytest.fixture
def first_name() -> FirstName:
    return FirstName("Никитос")


@pytest.fixture
def password() -> Password:
    return Password("super_secret1234")


@pytest.fixture
def phone() -> Phone:
    return Phone("+7 (000) 000-00-00")


@pytest.fixture
def email() -> Email:
    return Email("nikita.samkov@urfu.me")
