import re

from pydantic.dataclasses import dataclass


class InvalidEmailFormat(Exception):
    pass


@dataclass(eq=True, frozen=True)
class Email:
    value: str

    def __post_init_post_parse__(self) -> None:
        if not re.match(r"^\S+@\S+$", self.value):
            raise InvalidEmailFormat
