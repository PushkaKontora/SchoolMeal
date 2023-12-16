from dataclasses import dataclass

from app.shared.unit_of_work.abc import Context
from app.users.application.repositories import ISessionsRepository, IUsersRepository


@dataclass(frozen=True)
class UsersContext(Context):
    users: IUsersRepository
    sessions: ISessionsRepository
