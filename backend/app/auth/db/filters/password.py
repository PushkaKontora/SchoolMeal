from app.auth.db.models import Password
from app.database.specifications import FilterSpecification, TQuery


class ByUserId(FilterSpecification):
    def __init__(self, user_id: int):
        self._user_id = user_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Password.user_id == self._user_id)
