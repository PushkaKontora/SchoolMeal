from abc import ABC

from app.database.specifications import FilterSpecification


class PasswordByUserId(FilterSpecification, ABC):
    def __init__(self, user_id: int):
        self._user_id = user_id


class IssuedTokenByUserId(FilterSpecification, ABC):
    def __init__(self, user_id: int):
        self._user_id = user_id


class IssuedTokenByValue(FilterSpecification, ABC):
    def __init__(self, value: str):
        self._value = value
