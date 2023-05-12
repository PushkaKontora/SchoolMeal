from app.utils.error import Error


class BadCredentialsError(Error):
    @property
    def message(self) -> str:
        return "Incorrect login or password"

    @property
    def status_code(self) -> int:
        return 401


class InvalidTokenSignatureError(Error):
    @property
    def message(self) -> str:
        return "The token's signature was destroyed"


class NotFoundRefreshTokenError(Error):
    @property
    def message(self) -> str:
        return "The token was not created or was deleted by the service"


class RefreshUsingRevokedTokenError(Error):
    @property
    def message(self) -> str:
        return "The token is already revoked"


class TokenExpirationError(Error):
    @property
    def message(self) -> str:
        return "The token expired"
