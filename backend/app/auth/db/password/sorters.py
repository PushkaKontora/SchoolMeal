from app.auth.db.password.model import Password
from app.db.specifications import Specification, TQuery


class SortByCreationDateDESC(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.order_by(Password.created_at.desc())
