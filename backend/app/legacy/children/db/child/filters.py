from app.legacy.children.db.child.model import Child
from app.legacy.db.specifications import FilterSpecification, TQuery


class ByParentId(FilterSpecification):
    def __init__(self, parent_id: int):
        self._parent_id = parent_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Child.parent_id == self._parent_id)


class ByPupilId(FilterSpecification):
    def __init__(self, child_id: str):
        self._child_id = child_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Child.pupil_id == self._child_id)
