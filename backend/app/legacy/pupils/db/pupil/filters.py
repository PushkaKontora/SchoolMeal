from app.legacy.db.specifications import FilterSpecification, TQuery
from app.legacy.pupils.db.pupil.model import Pupil


class ById(FilterSpecification):
    def __init__(self, pupil_id: str):
        self._pupil_id = pupil_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Pupil.id == self._pupil_id)


class ByIds(FilterSpecification):
    def __init__(self, ids: set[str]):
        self._ids = ids

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Pupil.id.in_(self._ids))


class ByClassId(FilterSpecification):
    def __init__(self, class_id: int):
        self._class_id = class_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Pupil.class_id == self._class_id)
