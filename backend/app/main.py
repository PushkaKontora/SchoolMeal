from contextlib import asynccontextmanager
from typing import AsyncContextManager

from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.feedbacks.api.router import router as feedbacks_router
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.nutrition.api.router import router as nutrition_router
from app.nutrition.application.commands.submit_requests import SubmitRequestsCommand
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.db.container import DatabaseContainer
from app.shared.db.settings import AlchemySettings, DatabaseSettings
from app.shared.domain import timezones
from app.shared.fastapi.errors import default_handler
from app.shared.fastapi.settings import FastAPIConfig
from app.shared.objects_storage.local import LocalObjectsStorageSettings
from app.shared.processes.container import SchedulerContainer
from app.users.api.router import router as users_router
from app.users.infrastructure.dependencies import UsersContainer
from app.users.infrastructure.settings import JWTSettings


settings = FastAPIConfig()

database = DatabaseContainer()
database.database_config.from_pydantic(DatabaseSettings())
database.alchemy_config.from_pydantic(AlchemySettings())

nutrition = NutritionContainer(session=database.session)
nutrition.object_storage_config.from_pydantic(LocalObjectsStorageSettings())

feedbacks = FeedbacksContainer(session=database.session)

users = UsersContainer(session=database.session)
users.jwt_config.from_pydantic(JWTSettings())

for container in [nutrition, feedbacks, users]:
    container.check_dependencies()


@asynccontextmanager
async def startup_tasks(_: FastAPI) -> AsyncContextManager[None]:
    scheduler = SchedulerContainer().scheduler()
    scheduler.add_job(
        func=nutrition.submit_requests_command_handler().handle,
        trigger=CronTrigger(hour=15, timezone=timezones.yekaterinburg),
        kwargs={"command": SubmitRequestsCommand()},
    )

    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(
    docs_url="/docs" if settings.show_swagger_ui else None,
    lifespan=startup_tasks,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(Exception, default_handler)

app.include_router(users_router)
app.include_router(feedbacks_router)
app.include_router(nutrition_router)
