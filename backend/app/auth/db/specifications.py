from app.auth.db.filters import PasswordByUserId
from app.auth.db.sqlalchemy.filters import AlchemyPasswordByUserId


class PasswordsFilters:
    ByUserId: type[PasswordByUserId] = AlchemyPasswordByUserId
