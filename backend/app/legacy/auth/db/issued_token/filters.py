from app.legacy.auth.db.issued_token.model import IssuedToken
from app.legacy.db.specifications import FilterSpecification, TQuery


class ByUserId(FilterSpecification):
    def __init__(self, user_id: int):
        self._user_id = user_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(IssuedToken.user_id == self._user_id)


class ByValue(FilterSpecification):
    def __init__(self, value: str):
        self._value = value

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(IssuedToken.value == self._value)
