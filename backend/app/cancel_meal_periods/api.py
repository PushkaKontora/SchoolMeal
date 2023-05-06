from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from app.auth.presentation.middlewares import JWTAuth
from app.cancel_meal_periods.domain.services import PeriodService
from app.cancel_meal_periods.presentation.handlers import PeriodsHandlers
from app.cancel_meal_periods.presentation.routers import CancelMealPeriodsRouter


class CancelMealPeriodsAPI(DeclarativeContainer):
    jwt_auth = Dependency(instance_of=JWTAuth)

    period_service = Factory(PeriodService)

    periods_handlers = Factory(PeriodsHandlers, period_service=period_service)

    router = Factory(CancelMealPeriodsRouter, periods_handlers=periods_handlers, jwt_auth=jwt_auth)
