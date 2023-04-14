from abc import ABC

from app.database.specifications import FilterSpecification


class UserByLogin(FilterSpecification, ABC):
    def __init__(self, login: str):
        self._login = login
