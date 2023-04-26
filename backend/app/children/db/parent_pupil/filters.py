from app.children.db.parent_pupil.model import ParentPupil
from app.database.specifications import FilterSpecification, TQuery


class ByParentId(FilterSpecification):
    def __init__(self, parent_id: int):
        self._parent_id = parent_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(ParentPupil.parent_id == self._parent_id)


class ByPupilId(FilterSpecification):
    def __init__(self, child_id: str):
        self._child_id = child_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(ParentPupil.pupil_id == self._child_id)
