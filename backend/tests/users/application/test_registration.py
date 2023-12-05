import pytest

from app.users.application.services import PhoneBelongsToAnotherParent, UsersService
from app.users.domain.passwords import Password
from app.users.domain.phone import Phone
from app.users.domain.user import User


async def test_registration_parent(parent: User, password: Password, users_service: UsersService):
    phone = Phone("+7 (000) 000-00-00")
    user = await users_service.register_parent(
        parent.first_name.value, parent.last_name.value, phone.value, parent.email.value, password.value
    )

    assert user.last_name == parent.last_name
    assert user.first_name == parent.first_name
    assert user.login.value == phone.value
    assert user.phone == phone
    assert user.email == parent.email


async def test_registration_parent_using_not_unique_phone(
    parent: User, password: Password, users_service: UsersService
):
    with pytest.raises(PhoneBelongsToAnotherParent):
        await users_service.register_parent(
            first_name=parent.first_name.value,
            last_name=parent.last_name.value,
            phone=parent.phone.value,
            email=parent.email.value,
            password=password.value,
        )
