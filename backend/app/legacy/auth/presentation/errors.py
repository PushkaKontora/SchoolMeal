from app.legacy.utils.error import Error


class NotFoundRefreshTokenInCookiesError(Error):
    @property
    def message(self) -> str:
        return "A refresh token is not found in cookies"


class InvalidAuthorizationHeaderError(Error):
    @property
    def message(self) -> str:
        return "Invalid Authorization header"


class UnauthorizedError(Error):
    @property
    def message(self) -> str:
        return "Permission denied"

    @property
    def status_code(self) -> int:
        return 403
