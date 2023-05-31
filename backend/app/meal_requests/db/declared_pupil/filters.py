from app.db.specifications import FilterSpecification, TQuery
from app.meal_requests.db.declared_pupil.model import DeclaredPupil


class _ByRequestId(FilterSpecification):
    def __init__(self, request_id: int):
        self._request_id = request_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(DeclaredPupil.request_id == self._request_id)


class DeclaredPupilFilters:
    ByRequestId = _ByRequestId
