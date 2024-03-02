from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.container import ApplicationContainer
from app.db.settings import DatabaseSettings
from app.gateway import router
from app.shared.fastapi.errors import UnprocessableEntity, default_handler, unprocessable_entity_handler
from app.shared.fastapi.settings import FastAPIConfig


container = ApplicationContainer()
container.database_config.from_pydantic(DatabaseSettings())
container.wire()

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
