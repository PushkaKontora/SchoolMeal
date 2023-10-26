from uuid import UUID, uuid4

from pydantic import BaseModel

from app.common.domain.errors import DomainError
from app.users.domain.email import Email
from app.users.domain.login import Login
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import HashedPassword, Password
from app.users.domain.phone import Phone
from app.users.domain.role import Role


class NotVerifiedPasswordError(DomainError):
    pass


class User(BaseModel):
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
            raise NotVerifiedPasswordError("Неверный пароль для пользователя")

        return AuthenticatedUser.parse_obj(self)

    @classmethod
    def create_parent(
        cls, first_name: FirstName, last_name: LastName, phone: Phone, email: Email, password: Password
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
