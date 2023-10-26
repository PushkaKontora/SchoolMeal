from typing import Annotated

from fastapi import Depends

from app.common.api.dependencies import SessionDep
from app.users.application.repositories import ISessionsRepository, IUsersRepository
from app.users.infrastructure.db.repositories import SessionsRepository, UsersRepository


def _get_sessions_repository(session: SessionDep) -> ISessionsRepository:
    return SessionsRepository(session)


def _get_users_repository(session: SessionDep) -> IUsersRepository:
    return UsersRepository(session)


SessionsRepositoryDep = Annotated[ISessionsRepository, Depends(_get_sessions_repository)]
UsersRepositoryDep = Annotated[IUsersRepository, Depends(_get_users_repository)]
