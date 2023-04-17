from app.database.specifications import TQuery
from app.database.sqlalchemy.specifications import AlchemyFilterSpecification
from app.users.db.filters import UserById, UserByLogin
from app.users.db.sqlalchemy.models import User


class AlchemyUserById(UserById, AlchemyFilterSpecification):
    def to_query(self, query: TQuery) -> TQuery:
        return query.where(User.id == self._user_id)


class AlchemyUserByLogin(UserByLogin, AlchemyFilterSpecification):
    def to_query(self, query: TQuery) -> TQuery:
        return query.where(User.login == self._login)
