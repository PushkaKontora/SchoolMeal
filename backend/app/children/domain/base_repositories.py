from abc import ABC, abstractmethod

from app.children.db.models import ParentPupil
from app.database.base import Repository
from app.database.specifications import FilterSpecification


class BaseChildrenRepository(Repository[ParentPupil], ABC):
    @abstractmethod
    async def get_children_ids(self, specification: FilterSpecification) -> set[str]:
        raise NotImplementedError
