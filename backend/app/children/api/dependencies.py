from typing import Annotated

from fastapi import Depends

from app.children.application.services import ChildrenService
from app.children.application.unit_of_work import ChildrenContext
from app.children.infrastructure.db.repositories import ChildrenRepository, ParentsRepository
from app.shared.db.session import get_session_cls
from app.shared.fastapi.dependencies.settings import DatabaseSettingsDep
from app.shared.unit_of_work.alchemy import AlchemyUnitOfWork


def _get_children_service(database_settings: DatabaseSettingsDep) -> ChildrenService:
    return ChildrenService(
        unit_of_work=AlchemyUnitOfWork(
            session_factory=get_session_cls(settings=database_settings),
            context_factory=lambda session: ChildrenContext(
                parents=ParentsRepository(session),
                children=ChildrenRepository(session),
            ),
        )
    )


ChildrenServiceDep = Annotated[ChildrenService, Depends(_get_children_service)]
