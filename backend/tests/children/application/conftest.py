import pytest

from app.children.application.repositories import IChildrenRepository, IParentsRepository
from app.children.domain.child import Child
from app.children.domain.parent import Parent
from tests.children.application.repositories import LocalChildrenRepository, LocalParentsRepository


@pytest.fixture
def parents_repository(parent: Parent) -> IParentsRepository:
    return LocalParentsRepository(parents=[parent])


@pytest.fixture
def children_repository(child: Child) -> IChildrenRepository:
    return LocalChildrenRepository(children=[child])
