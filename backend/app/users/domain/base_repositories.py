from abc import ABC

from app.database.base import Repository
from app.users.db.models import User


class BaseUsersRepository(Repository[User], ABC):
    pass
