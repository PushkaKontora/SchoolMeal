from app.users.db.filters import UserByLogin
from app.users.db.sqlalchemy.filters import AlchemyUserByLogin


class UsersFilter:
    ByLogin: type[UserByLogin] = AlchemyUserByLogin
