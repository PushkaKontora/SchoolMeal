from typing import Annotated

from fastapi import Depends

from app.children.application.repositories import IChildrenRepository, IParentsRepository
from app.children.infrastructure.db.repositories import ChildrenRepository, ParentsRepository
from app.common.api.dependencies.db import SessionDep


def _get_parents_repository(session: SessionDep) -> IParentsRepository:
    return ParentsRepository(session)


def _get_children_repository(session: SessionDep) -> IChildrenRepository:
    return ChildrenRepository(session)


ParentsRepositoryDep = Annotated[IParentsRepository, Depends(_get_parents_repository)]
ChildrenRepositoryDep = Annotated[IChildrenRepository, Depends(_get_children_repository)]
