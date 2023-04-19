from app.database.specifications import FilterSpecification, TQuery
from app.users.db.models import User


class ById(FilterSpecification):
    def __init__(self, user_id: int):
        self._user_id = user_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(User.id == self._user_id)


class ByLogin(FilterSpecification):
    def __init__(self, login: str):
        self._login = login

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(User.login == self._login)
