from typing import Annotated

from fastapi import Depends

from app.shared.fastapi.dependencies.db import SessionDep
from app.shared.fastapi.dependencies.unit_of_work import UnitOfWorkDep
from app.users.api.dependencies.settings import JWTSettingsDep
from app.users.application.services import SessionsService, UsersService
from app.users.infrastructure.db.repositories import SessionsRepository, UsersRepository


def _get_sessions_service(
    unit_of_work: UnitOfWorkDep, session: SessionDep, settings: JWTSettingsDep
) -> SessionsService:
    return SessionsService(
        unit_of_work=unit_of_work,
        sessions_repository=SessionsRepository(session),
        secret=settings.secret.get_secret_value(),
    )


def _get_users_service(
    unit_of_work: UnitOfWorkDep, session: SessionDep, settings: JWTSettingsDep, sessions_service: "SessionsServiceDep"
) -> UsersService:
    return UsersService(
        unit_of_work=unit_of_work,
        users_repository=UsersRepository(session),
        secret=settings.secret.get_secret_value(),
        sessions_service=sessions_service,
    )


SessionsServiceDep = Annotated[SessionsService, Depends(_get_sessions_service)]
UsersServiceDep = Annotated[UsersService, Depends(_get_users_service)]
