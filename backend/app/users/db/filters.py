from abc import ABC

from app.database.specifications import FilterSpecification


class UserById(FilterSpecification, ABC):
    def __init__(self, user_id: int):
        self._user_id = user_id


class UserByLogin(FilterSpecification, ABC):
    def __init__(self, login: str):
        self._login = login
