from abc import ABC, abstractmethod

from app.identity.domain.jwt import Payload
from app.identity.domain.rest import Method


class IAuthorization(ABC):
    @abstractmethod
    def authorize(self, payload: Payload, uri: str, method: Method) -> bool:
        raise NotImplementedError
