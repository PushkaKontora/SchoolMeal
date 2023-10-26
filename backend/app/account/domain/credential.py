from uuid import UUID

from pydantic import BaseModel

from app.account.domain.login import Login
from app.account.domain.passwords import HashedPassword, Password
from app.common.domain.errors import DomainError


class IncorrectPasswordError(DomainError):
    pass


class Credential(BaseModel):
    id: UUID
    login: Login
    password: HashedPassword

    def authenticate(self, password: Password) -> "AuthenticatedCredential":
        if not self.password.verify(password):
            raise IncorrectPasswordError("Пароль не совпадает с действительным")

        return AuthenticatedCredential(id=self.id, login=self.login, password=self.password)


class AuthenticatedCredential(Credential):
    pass
