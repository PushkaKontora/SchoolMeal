from unittest.mock import AsyncMock

import pytest

from app.children.application.services import ChildrenService
from app.children.domain.child import Child
from app.children.domain.parent import Parent
from tests.children.application.repositories import LocalChildrenRepository, LocalParentsRepository


@pytest.fixture
def children_service(parent: Parent, child: Child) -> ChildrenService:
    return ChildrenService(
        unit_of_work=AsyncMock(),
        parents_repository=LocalParentsRepository(parents=[parent]),
        children_repository=LocalChildrenRepository(children=[child]),
    )
