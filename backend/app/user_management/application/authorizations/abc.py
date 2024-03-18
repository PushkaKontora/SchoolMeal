from abc import ABC, abstractmethod

from app.user_management.domain.jwt import Payload
from app.user_management.domain.rest import Method


class IAuthorization(ABC):
    @abstractmethod
    def authorize(self, payload: Payload, uri: str, method: Method) -> bool:
        raise NotImplementedError
