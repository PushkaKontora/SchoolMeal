from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class APIError(ABC):
    message: str


class ValidationError(APIError):
    pass
