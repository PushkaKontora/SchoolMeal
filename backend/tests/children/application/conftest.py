import pytest

from app.children.application.services import ChildrenService
from app.children.application.unit_of_work import ChildrenContext
from app.children.domain.child import Child
from app.children.domain.parent import Parent
from tests.children.application.repositories import LocalChildrenRepository, LocalParentsRepository
from tests.unit_of_work import LocalUnitOfWork


@pytest.fixture
def children_service(parent: Parent, child: Child) -> ChildrenService:
    return ChildrenService(
        unit_of_work=LocalUnitOfWork(
            lambda: ChildrenContext(
                parents=LocalParentsRepository([parent]),
                children=LocalChildrenRepository([child]),
            )
        )
    )
