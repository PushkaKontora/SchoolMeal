from app.database.specifications import TQuery
from app.database.sqlalchemy.specifications import AlchemyFilterSpecification
from app.users.db.filters import UserByLogin
from app.users.db.sqlalchemy.models import User


class AlchemyUserByLogin(UserByLogin, AlchemyFilterSpecification):
    def to_query(self, query: TQuery) -> TQuery:
        return query.filter(User.login == self._login)
