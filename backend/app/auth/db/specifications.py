from app.auth.db.filters import IssuedTokenByUserId, IssuedTokenByValue, PasswordByUserId
from app.auth.db.sqlalchemy.filters import (
    AlchemyIssuedTokenByUserId,
    AlchemyIssuedTokenByValue,
    AlchemyPasswordByUserId,
)


class PasswordsFilter:
    ByUserId: type[PasswordByUserId] = AlchemyPasswordByUserId


class IssuedTokensFilter:
    ByUserId: type[IssuedTokenByUserId] = AlchemyIssuedTokenByUserId
    ByValue: type[IssuedTokenByValue] = AlchemyIssuedTokenByValue
