from typing import Annotated

from fastapi import Depends

from app.account.application.repositories import ICredentialsRepository, ISessionsRepository, IUsersRepository
from app.account.infrastructure.db.repositories import CredentialsRepository, SessionsRepository, UsersRepository
from app.common.api.dependencies import SessionDep


def _get_credentials_repository(session: SessionDep) -> ICredentialsRepository:
    return CredentialsRepository(session)


def _get_sessions_repository(session: SessionDep) -> ISessionsRepository:
    return SessionsRepository(session)


def _get_users_repository(session: SessionDep) -> IUsersRepository:
    return UsersRepository(session)


CredentialsRepositoryDep = Annotated[ICredentialsRepository, Depends(_get_credentials_repository)]
SessionsRepositoryDep = Annotated[ISessionsRepository, Depends(_get_sessions_repository)]
UsersRepositoryDep = Annotated[IUsersRepository, Depends(_get_users_repository)]
