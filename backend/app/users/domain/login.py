from pydantic.dataclasses import dataclass


class LoginIsEmpty(Exception):
    pass


@dataclass(eq=True, frozen=True)
class Login:
    value: str

    def __post_init_post_parse__(self) -> None:
        if not self.value:
            raise LoginIsEmpty
