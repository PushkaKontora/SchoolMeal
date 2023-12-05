from typing import Annotated

from fastapi import Depends

from app.children.application.services import ChildrenService
from app.children.infrastructure.db.repositories import ChildrenRepository, ParentsRepository
from app.shared.fastapi.dependencies.db import SessionDep
from app.shared.fastapi.dependencies.unit_of_work import UnitOfWorkDep


def _get_children_service(unit_of_work: UnitOfWorkDep, session: SessionDep) -> ChildrenService:
    return ChildrenService(
        unit_of_work=unit_of_work,
        parents_repository=ParentsRepository(session),
        children_repository=ChildrenRepository(session),
    )


ChildrenServiceDep = Annotated[ChildrenService, Depends(_get_children_service)]
