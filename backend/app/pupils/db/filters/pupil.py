from app.database.specifications import FilterSpecification, TQuery
from app.pupils.db.models import Pupil


class ById(FilterSpecification):
    def __init__(self, pupil_id: str):
        self._pupil_id = pupil_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Pupil.id == self._pupil_id)
