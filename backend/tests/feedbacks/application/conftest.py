from uuid import uuid4

import pytest

from app.feedbacks.application.repositories import ICanteenRepository, IFeedbackRepository
from app.feedbacks.application.services import CanteenService, FeedbackService
from app.feedbacks.domain.canteen import Canteen
from app.shared.fastapi.schemas import AuthorizedUser, RoleOut
from tests.feedbacks.application.repositories import LocalCanteenRepository, LocalFeedbackRepository


@pytest.fixture
def canteen() -> Canteen:
    return Canteen(id=uuid4())


@pytest.fixture
def authorized_user() -> AuthorizedUser:
    return AuthorizedUser(id=uuid4(), role=RoleOut.PARENT)


@pytest.fixture
def canteen_repository(canteen: Canteen) -> ICanteenRepository:
    return LocalCanteenRepository(canteens=[canteen])


@pytest.fixture
def canteen_service(canteen_repository: ICanteenRepository) -> CanteenService:
    return CanteenService(repository=canteen_repository)


@pytest.fixture
def feedback_repository() -> IFeedbackRepository:
    return LocalFeedbackRepository()


@pytest.fixture
def feedback_service(feedback_repository: IFeedbackRepository, canteen_service: CanteenService) -> FeedbackService:
    return FeedbackService(repository=feedback_repository, canteen_service=canteen_service)
