import re

from pydantic.dataclasses import dataclass

from app.users.domain.login import Login


EXAMPLE = "+7 (000) 000-00-00"


class InvalidPhoneFormat(Exception):
    pass


@dataclass(eq=True, frozen=True)
class Phone:
    value: str

    def __post_init_post_parse__(self) -> None:
        if not re.match(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$", self.value):
            raise InvalidPhoneFormat

    def as_login(self) -> Login:
        return Login(self.value)
