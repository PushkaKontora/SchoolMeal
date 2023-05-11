from app.database.specifications import FilterSpecification, TQuery
from app.users.db.user.model import User


class ByUserId(FilterSpecification):
    def __init__(self, user_id: int):
        self._user_id = user_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(User.id == self._user_id)


class ByLogin(FilterSpecification):
    def __init__(self, login: str):
        self._login = login

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(User.login == self._login)


class ByPhone(FilterSpecification):
    def __init__(self, phone: str):
        self._phone = phone

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(User.phone == self._phone)


class ByEmail(FilterSpecification):
    def __init__(self, email: str):
        self._email = email

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(User.email == self._email)
