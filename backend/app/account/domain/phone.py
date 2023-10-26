import re

from pydantic.dataclasses import dataclass

from app.account.domain.login import Login
from app.common.domain.errors import DomainError


class InvalidPhoneError(DomainError):
    pass


@dataclass(eq=True, frozen=True)
class Phone:
    value: str

    def __post_init_post_parse__(self) -> None:
        if not re.match(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$", self.value):
            raise InvalidPhoneError("Номер не соответствует маске '+7 (000) 000-00-00'")

    def as_login(self) -> Login:
        return Login(self.value)
