from app.account.application.repositories import IUsersRepository, NotUniqueLoginError
from app.account.domain.email import Email
from app.account.domain.names import FirstName, LastName
from app.account.domain.passwords import Password
from app.account.domain.phone import Phone
from app.account.domain.user import User


class AlreadyRegisteredPhoneError(Exception):
    pass


async def register_parent(
    first_name: FirstName,
    last_name: LastName,
    phone: Phone,
    email: Email,
    password: Password,
    users_repository: IUsersRepository,
) -> User:
    """
    :raise AlreadyRegisteredPhoneError: телефон уже зарегистрирован
    """

    parent = User.create_parent(first_name, last_name, phone, email, password)

    try:
        await users_repository.save(parent)

    except NotUniqueLoginError as error:
        raise AlreadyRegisteredPhoneError("Телефон уже зарегистрирован") from error

    return parent
