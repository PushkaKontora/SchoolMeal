from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.container import AlchemyORM
from app.db.settings import DatabaseSettings
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.gateway import router
from app.gateway.errors import UnprocessableEntity, default_handler, unprocessable_entity_handler
from app.nutrition.infrastructure.dependencies import NutritionContainer
from app.shared.fastapi.settings import FastAPIConfig


alchemy = AlchemyORM()
alchemy.config.from_pydantic(DatabaseSettings())

nutrition = NutritionContainer(alchemy=alchemy)
feedbacks = FeedbacksContainer(alchemy=alchemy)

for module in [nutrition, feedbacks]:
    module.check_dependencies()
    module.wire()

settings = FastAPIConfig()
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
