from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.db.container import AlchemyORM
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.nutrition.infrastructure.dependencies import NutritionContainer


class ApplicationContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app.gateway.dependencies"], auto_wire=False)

    database_config = providers.Configuration(strict=True)
    alchemy = providers.Container(AlchemyORM, config=database_config)

    feedbacks = providers.Container(FeedbacksContainer, alchemy=alchemy)
    nutrition = providers.Container(NutritionContainer, alchemy=alchemy)
