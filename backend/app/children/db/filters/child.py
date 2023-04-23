from app.children.db.models import Child
from app.database.specifications import FilterSpecification, TQuery


class ParentById(FilterSpecification):
    def __init__(self, parent_id: int):
        self._parent_id = parent_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Child.parent_id == self._parent_id)


class ChildById(FilterSpecification):
    def __init__(self, child_id: str):
        self._child_id = child_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Child.pupil_id == self._child_id)
