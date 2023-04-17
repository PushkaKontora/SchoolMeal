from app.users.db.filters import UserById, UserByLogin
from app.users.db.sqlalchemy.filters import AlchemyUserById, AlchemyUserByLogin


class UsersFilter:
    ById: type[UserById] = AlchemyUserById
    ByLogin: type[UserByLogin] = AlchemyUserByLogin
