from uuid import uuid4

import pytest

from app.feedbacks.application.services import FeedbacksService
from app.feedbacks.application.unit_of_work import FeedbacksContext
from app.feedbacks.domain.canteen import Canteen
from app.shared.fastapi.schemas import AuthorizedUser, RoleOut
from tests.feedbacks.application.repositories import LocalCanteensRepository, LocalFeedbacksRepository
from tests.unit_of_work import LocalUnitOfWork


@pytest.fixture
def canteen() -> Canteen:
    return Canteen(id=uuid4())


@pytest.fixture
def authorized_user() -> AuthorizedUser:
    return AuthorizedUser(id=uuid4(), role=RoleOut.PARENT)


@pytest.fixture
def feedbacks_service(canteen: Canteen) -> FeedbacksService:
    return FeedbacksService(
        unit_of_work=LocalUnitOfWork(
            lambda: FeedbacksContext(
                feedbacks=LocalFeedbacksRepository(),
                canteens=LocalCanteensRepository([canteen]),
            )
        )
    )
