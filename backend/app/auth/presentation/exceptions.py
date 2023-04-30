from app.exceptions import APIException


class NotFoundRefreshCookieException(APIException):
    @property
    def message(self) -> str:
        return "A refresh token is not found in cookies"


class InvalidBearerCredentialsException(APIException):
    @property
    def message(self) -> str:
        return "Invalid Authorization header"


class UnauthorizedException(APIException):
    @property
    def message(self) -> str:
        return "Permission denied"

    @property
    def status_code(self) -> int:
        return 403
