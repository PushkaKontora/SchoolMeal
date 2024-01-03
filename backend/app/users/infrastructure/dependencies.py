from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Dependency, Factory
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork
from app.users import api, application
from app.users.application.services import UsersService
from app.users.application.unit_of_work import UsersContext
from app.users.infrastructure.db.repositories import SessionsRepository, UsersRepository


class UsersContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[api, application])

    session = Dependency(instance_of=AsyncSession)

    jwt_config = Configuration(strict=True)

    unit_of_work = Factory(
        AlchemyUnitOfWork,
        session_factory=session.provider,
        context_factory=lambda session: UsersContext(
            users=UsersRepository(session),
            sessions=SessionsRepository(session),
        ),
    )

    service = Factory(
        UsersService,
        unit_of_work=unit_of_work,
        secret=jwt_config.secret,
    )
