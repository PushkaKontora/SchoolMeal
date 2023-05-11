from sqlalchemy.orm import joinedload

from app.database.specifications import Specification, TQuery
from app.portions.db.portion.model import Portion


class WithFood(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(Portion.food))
