from abc import ABC
from typing import Callable

from sqlalchemy import Select, and_, not_, or_

from app.database.specifications import FilterSpecification


class AlchemyFilterSpecification(FilterSpecification, ABC):
    def __and__(self, other: FilterSpecification) -> FilterSpecification:
        return CompositeFilterSpecification(and_, self, other)

    def __or__(self, other: FilterSpecification) -> FilterSpecification:
        return CompositeFilterSpecification(or_, self, other)

    def __invert__(self) -> FilterSpecification:
        return CompositeFilterSpecification(not_, self)


class CompositeFilterSpecification(AlchemyFilterSpecification, ABC):
    def __init__(self, func: Callable, *specifications: FilterSpecification):
        self._specifications = specifications
        self._func = func

    def to_query(self, query: Select) -> Select:
        specs = [spec.to_query(query=Select()).whereclause for spec in self._specifications]

        return query.filter(self._func(*specs))
