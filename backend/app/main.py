from contextlib import asynccontextmanager
from typing import AsyncIterator

from apscheduler.schedulers.base import BaseScheduler
from dependency_injector.containers import DeclarativeContainer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.container import AlchemyORM
from app.db.settings import DatabaseSettings
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.gateway import router
from app.gateway.errors import UnprocessableEntity, default_handler, unprocessable_entity_handler
from app.identity.application.tasks import scheduler as identity_scheduler
from app.identity.infrastructure.dependencies import IdentityContainer
from app.nutrition.application.tasks import scheduler as nutrition_scheduler
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.fastapi.settings import FastAPIConfig
from app.structure.infrastructure.dependencies import StructureContainer


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    alchemy = AlchemyORM()
    alchemy.config.from_pydantic(DatabaseSettings())

    modules: list[DeclarativeContainer] = [
        NutritionContainer(alchemy=alchemy),
        FeedbacksContainer(alchemy=alchemy),
        StructureContainer(alchemy=alchemy),
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
app.include_router(router)
