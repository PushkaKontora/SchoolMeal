import pytest

from app.users.application.repositories import IUsersRepository
from app.users.application.use_cases.registration import AlreadyRegisteredPhoneError, register_parent
from app.users.domain.passwords import Password
from app.users.domain.phone import Phone
from app.users.domain.user import User


async def test_registration_parent(
    parent: User,
    password: Password,
    users_repository: IUsersRepository,
):
    phone = Phone("+7 (000) 000-00-00")
    user = await register_parent(parent.first_name, parent.last_name, phone, parent.email, password, users_repository)

    assert user.last_name == parent.last_name
    assert user.first_name == parent.first_name
    assert user.login.value == phone.value
    assert user.phone == phone
    assert user.email == parent.email


async def test_registration_parent_using_not_unique_phone(
    parent: User,
    password: Password,
    users_repository: IUsersRepository,
):
    with pytest.raises(AlreadyRegisteredPhoneError) as error_info:
        await register_parent(
            first_name=parent.first_name,
            last_name=parent.last_name,
            phone=parent.phone,
            email=parent.email,
            password=password,
            users_repository=users_repository,
        )

    assert str(error_info.value) == "Телефон уже зарегистрирован"
