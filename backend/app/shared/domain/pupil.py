import secrets
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class PupilID:
    value: str

    @classmethod
    def generate(cls) -> "PupilID":
        return cls(secrets.token_hex(10))
