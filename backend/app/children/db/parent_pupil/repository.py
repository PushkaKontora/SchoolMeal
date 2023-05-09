from sqlalchemy import select

from app.children.db.parent_pupil.model import ParentPupil
from app.children.domain.base_repositories import BaseChildrenRepository
from app.database.specifications import FilterSpecification


class ChildrenRepository(BaseChildrenRepository):
    async def get_children_ids(self, specification: FilterSpecification) -> set[str]:
        query = specification(select(ParentPupil).with_only_columns(ParentPupil.pupil_id))

        return set(await self.session.scalars(query))
