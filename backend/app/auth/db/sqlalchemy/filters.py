from app.auth.db.filters import IssuedTokenByUserId, IssuedTokenByValue, PasswordByUserId
from app.auth.db.sqlalchemy.models import IssuedToken, Password
from app.database.specifications import TQuery
from app.database.sqlalchemy.specifications import AlchemyFilterSpecification


class AlchemyPasswordByUserId(PasswordByUserId, AlchemyFilterSpecification):
    def to_query(self, query: TQuery) -> TQuery:
        return query.where(Password.user_id == self._user_id)


class AlchemyIssuedTokenByUserId(IssuedTokenByUserId, AlchemyFilterSpecification):
    def to_query(self, query: TQuery) -> TQuery:
        return query.where(IssuedToken.user_id == self._user_id)


class AlchemyIssuedTokenByValue(IssuedTokenByValue, AlchemyFilterSpecification):
    def to_query(self, query: TQuery) -> TQuery:
        return query.where(IssuedToken.value == self._value)
