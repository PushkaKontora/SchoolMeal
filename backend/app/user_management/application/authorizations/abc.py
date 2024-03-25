from abc import ABC, abstractmethod

from app.user_management.domain.jwt import AccessToken
from app.user_management.domain.rest import Method


class IAuthorization(ABC):
    @abstractmethod
    def authorize(self, token: AccessToken, uri: str, method: Method) -> bool:
        raise NotImplementedError
