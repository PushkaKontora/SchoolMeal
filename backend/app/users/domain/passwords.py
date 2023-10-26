import bcrypt
from pydantic.dataclasses import dataclass

from app.common.domain.errors import DomainError


class InvalidPasswordError(DomainError):
    pass


@dataclass(eq=True, frozen=True)
class Password:
    value: str

    def __post_init_post_parse__(self) -> None:
        if not self.value:
            raise InvalidPasswordError("Пароль не может быть пустым")

    def hash(self) -> "HashedPassword":
        return HashedPassword(bcrypt.hashpw(self.value.encode(), bcrypt.gensalt()))


@dataclass(eq=True, frozen=True)
class HashedPassword:
    value: bytes

    def verify(self, password: Password) -> bool:
        return bcrypt.checkpw(password.value.encode(), self.value)
