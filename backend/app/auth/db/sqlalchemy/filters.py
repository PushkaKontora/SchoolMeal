from app.auth.db.filters import PasswordByUserId
from app.auth.db.sqlalchemy.models import Password
from app.database.specifications import TQuery
from app.database.sqlalchemy.specifications import AlchemyFilterSpecification


class AlchemyPasswordByUserId(PasswordByUserId, AlchemyFilterSpecification):
    def to_query(self, query: TQuery) -> TQuery:
        return query.filter(Password.user_id == self._user_id)
