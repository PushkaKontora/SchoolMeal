from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from app.container import ApplicationContainer
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.ipc.feedbacks.api import IFeedbacksAPI
from app.ipc.nutrition.api import INutritionAPI
from app.nutrition.infrastructure.dependencies import NutritionContainer


@inject
def get_feedbacks_api(
    container: FeedbacksContainer = Depends(Provide[ApplicationContainer.feedbacks]),
) -> IFeedbacksAPI:
    return container.api()


@inject
def get_nutrition_api(
    container: NutritionContainer = Depends(Provide[ApplicationContainer.nutrition]),
) -> INutritionAPI:
    return container.api()


FeedbacksAPIDep = Annotated[IFeedbacksAPI, Depends(get_feedbacks_api)]
NutritionAPIDep = Annotated[INutritionAPI, Depends(get_nutrition_api)]
