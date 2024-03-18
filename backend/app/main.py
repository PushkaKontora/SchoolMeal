from contextlib import asynccontextmanager
from typing import AsyncIterator

from apscheduler.schedulers.base import BaseScheduler
from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.container import AlchemyORM
from app.db.settings import DatabaseSettings
from app.feedbacks.api import router as feedbacks_api
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.nutrition.api import router as nutrition_api
from app.nutrition.application.tasks import scheduler as nutrition_scheduler
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.api.errors import UnprocessableEntity, default_handler, unprocessable_entity_handler
from app.shared.fastapi.settings import FastAPIConfig
from app.user_management.api import router as identity_api
from app.user_management.application.tasks import scheduler as identity_scheduler
from app.user_management.infrastructure.dependencies import IdentityContainer


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    alchemy = AlchemyORM()
    alchemy.config.from_pydantic(DatabaseSettings())

    modules: list[DeclarativeContainer] = [
        NutritionContainer(alchemy=alchemy),
        FeedbacksContainer(alchemy=alchemy),
        IdentityContainer(alchemy=alchemy),
    ]
    schedulers: list[BaseScheduler] = [nutrition_scheduler, identity_scheduler]

    for module in modules:
        module.check_dependencies()
        module.wire()

    for scheduler in schedulers:
        scheduler.start()

    yield

    for scheduler in schedulers:
        scheduler.shutdown()


settings = FastAPIConfig()

app = FastAPI(
    docs_url="/docs" if settings.show_swagger_ui else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(UnprocessableEntity, unprocessable_entity_handler)
app.add_exception_handler(Exception, default_handler)

app.include_router(identity_api, prefix="/user-management", tags=["User Management"])
app.include_router(nutrition_api, prefix="/nutrition", tags=["Nutrition"])
app.include_router(feedbacks_api, prefix="/feedbacks", tags=["Feedbacks"])
