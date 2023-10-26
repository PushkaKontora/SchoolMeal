from app.common.api.schemas import FrontendModel
from app.common.infrastructure.settings import jwt
from app.users.domain.login import InvalidLoginError, Login
from app.users.domain.passwords import InvalidPasswordError, Password
from app.users.domain.tokens import AccessToken


class InvalidCredentialError(Exception):
    pass


class CredentialIn(FrontendModel):
    login: str
    password: str

    def to_model(self) -> tuple[Login, Password]:
        """
        :raise InvalidCredentialError
        """

        try:
            return Login(self.login), Password(self.password)
        except (InvalidLoginError, InvalidPasswordError) as error:
            raise InvalidCredentialError(str(error))


class AccessTokenOut(FrontendModel):
    access_token: str

    @classmethod
    def from_model(cls, access: AccessToken) -> "AccessTokenOut":
        return cls(access_token=access.encode(jwt.secret.get_secret_value()))
