from app.exceptions import APIException


class BadCredentialsException(APIException):
    @property
    def message(self) -> str:
        return "Incorrect login or password"

    @property
    def status_code(self) -> int:
        return 401


class InvalidTokenSignatureException(APIException):
    @property
    def message(self) -> str:
        return "The token's signature was destroyed"


class NotFoundRefreshTokenException(APIException):
    @property
    def message(self) -> str:
        return "The token was not created or was deleted by the service"


class RefreshWithRevokedTokenException(APIException):
    @property
    def message(self) -> str:
        return "The token is already revoked"


class TokenExpirationException(APIException):
    @property
    def message(self) -> str:
        return "The token expired"


class UnknownTokenTypeException(Exception):
    pass
