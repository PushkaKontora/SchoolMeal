from pydantic.dataclasses import dataclass

from app.common.domain.errors import DomainError


class InvalidLoginError(DomainError):
    pass


@dataclass(eq=True, frozen=True)
class Login:
    value: str

    def __post_init_post_parse__(self) -> None:
        if not self.value:
            raise InvalidLoginError("Логин не может быть пустым")
