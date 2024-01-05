from pydantic.dataclasses import dataclass

from app.shared.domain.abc import ValueObject


class LoginIsEmpty(Exception):
    pass


@dataclass(eq=True, frozen=True)
class Login(ValueObject):
    value: str

    def __post_init_post_parse__(self) -> None:
        if not self.value:
            raise LoginIsEmpty
