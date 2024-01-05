from uuid import UUID, uuid4

from pydantic.dataclasses import dataclass

from app.shared.domain.abc import Entity
from app.users.domain.email import Email
from app.users.domain.login import Login
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import HashedPassword, Password, StrictPassword
from app.users.domain.phone import Phone
from app.users.domain.role import Role


class PasswordIsNotVerified(Exception):
    pass


@dataclass
class User(Entity):
    id: UUID
    login: Login
    password: HashedPassword
    last_name: LastName
    first_name: FirstName
    role: Role
    phone: Phone
    email: Email

    def authenticate(self, password: Password) -> "AuthenticatedUser":
        if not self.password.verify(password):
            raise PasswordIsNotVerified

        return AuthenticatedUser(
            id=self.id,
            login=self.login,
            password=self.password,
            last_name=self.last_name,
            first_name=self.first_name,
            role=self.role,
            phone=self.phone,
            email=self.email,
        )

    @classmethod
    def create_parent(
        cls, first_name: FirstName, last_name: LastName, phone: Phone, email: Email, password: StrictPassword
    ) -> "User":
        return cls(
            id=uuid4(),
            login=phone.as_login(),
            password=password.hash(),
            last_name=last_name,
            first_name=first_name,
            role=Role.PARENT,
            phone=phone,
            email=email,
        )


class AuthenticatedUser(User):
    pass
