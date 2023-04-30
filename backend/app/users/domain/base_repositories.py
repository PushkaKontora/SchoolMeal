from abc import ABC

from app.database.base import Repository
from app.users.db.user.model import User


class BaseUsersRepository(Repository[User], ABC):
    pass
