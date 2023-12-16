from typing import Annotated

from fastapi import Depends

from app.shared.db.session import get_session_cls
from app.shared.fastapi.dependencies.settings import DatabaseSettingsDep
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork
from app.users.api.dependencies.settings import JWTSettingsDep
from app.users.application.services import UsersService
from app.users.application.unit_of_work import UsersContext
from app.users.infrastructure.db.repositories import SessionsRepository, UsersRepository


def _get_users_service(database_settings: DatabaseSettingsDep, jwt_settings: JWTSettingsDep) -> UsersService:
    return UsersService(
        unit_of_work=AlchemyUnitOfWork(
            session_factory=get_session_cls(settings=database_settings),
            context_factory=lambda session: UsersContext(
                users=UsersRepository(session),
                sessions=SessionsRepository(session),
            ),
        ),
        secret=jwt_settings.secret.get_secret_value(),
    )


UsersServiceDep = Annotated[UsersService, Depends(_get_users_service)]
