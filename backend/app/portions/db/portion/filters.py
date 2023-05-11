from app.database.specifications import FilterSpecification, TQuery
from app.portions.db.portion.model import Portion


class ByPortionId(FilterSpecification):
    def __init__(self, portion_id: int):
        self._portion_id = portion_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Portion.id == self._portion_id)
