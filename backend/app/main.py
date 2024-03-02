from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.gateway import router
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.db.container import DatabaseContainer
from app.shared.db.settings import AlchemySettings, DatabaseSettings
from app.shared.fastapi.errors import UnprocessableEntity, default_handler, unprocessable_entity_handler
from app.shared.fastapi.settings import FastAPIConfig
from app.shared.objects_storage.local import LocalObjectsStorageSettings


settings = FastAPIConfig()

database = DatabaseContainer()
database.database_config.from_pydantic(DatabaseSettings())
database.alchemy_config.from_pydantic(AlchemySettings())

nutrition = NutritionContainer(session=database.session)
nutrition.object_storage_config.from_pydantic(LocalObjectsStorageSettings())

feedbacks = FeedbacksContainer(session=database.session)

for container in [nutrition, feedbacks]:
    container.check_dependencies()


app = FastAPI(
    docs_url="/docs" if settings.show_swagger_ui else None,
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
