from app.common.gateway.errors import Error


class PhoneValidationError(Error):
    @property
    def message(self) -> str:
        return "Неверный формат номера телефона. Ожидался формат: +, цифра 1-9 и 11 цифр"

    @property
    def status_code(self) -> int:
        return 422


class PasswordValidationError(Error):
    @property
    def message(self) -> str:
        return "Пароль не содержит символов"

    @property
    def status_code(self) -> int:
        return 422


class FirstNameValidationError(Error):
    @property
    def message(self) -> str:
        return "Имя не содержит символов"

    @property
    def status_code(self) -> int:
        return 422


class LastNameValidationError(Error):
    @property
    def message(self) -> str:
        return "Фамилия не содержит символов"

    @property
    def status_code(self) -> int:
        return 422


class EmailValidationError(Error):
    @property
    def message(self) -> str:
        return "Неверный формат элетронной почты. Ожидался формат: уникальное имя, @ и домен"

    @property
    def status_code(self) -> int:
        return 422


class NotUniqueLoginOrPhoneOrEmailError(Error):
    @property
    def message(self) -> str:
        return "Логин, телефон или адрес электронной почты уже используются"

    @property
    def status_code(self) -> int:
        return 400
