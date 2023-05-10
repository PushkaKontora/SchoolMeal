from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from app.foods.domain.services import PortionService
from app.foods.presentation.handlers import PortionsHandlers
from app.foods.presentation.routers import PortionsRouter


class FoodAPI(DeclarativeContainer):
    portion_service = Factory(PortionService)

    portions_handlers = Factory(PortionsHandlers, portion_service=portion_service)

    portions_router = Factory(PortionsRouter, portions_handlers=portions_handlers)
