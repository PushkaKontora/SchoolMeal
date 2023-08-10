from app.common.gateway.errors import Error


class LoginValidationError(Error):
    @property
    def message(self) -> str:
        return "Логин должен содержать хоть один символ"

    @property
    def status_code(self) -> int:
        return 422


class PasswordValidationError(Error):
    @property
    def message(self) -> str:
        return "Пароль должен содержать хоть один символ"

    @property
    def status_code(self) -> int:
        return 422


class WrongLoginOrPasswordError(Error):
    @property
    def message(self) -> str:
        return "Неверный логин или пароль"

    @property
    def status_code(self) -> int:
        return 404


class LostRefreshTokenError(Error):
    @property
    def message(self) -> str:
        return "Потеряна кука с рефреш-токеном"

    @property
    def status_code(self) -> int:
        return 422


class InvalidRefreshTokenError(Error):
    @property
    def message(self) -> str:
        return "Невозомжно обновить токены. Необходимо заново аутентифицироваться"

    @property
    def status_code(self) -> int:
        return 400
