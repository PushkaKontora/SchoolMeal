from dataclasses import dataclass

from app.children.application.repositories import IChildrenRepository, IParentsRepository
from app.shared.unit_of_work.abc import Context


@dataclass(frozen=True)
class ChildrenContext(Context):
    parents: IParentsRepository
    children: IChildrenRepository
