from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.children.api.router import router as pupils_router
from app.common.api import responses
from app.common.api.errors import default_handler
from app.common.infrastructure.settings import ServiceSettings
from app.feedbacks.api.router import router as feedbacks_router
from app.users.api.router import router as users_router


settings = ServiceSettings()

app = FastAPI(
    docs_url="/docs" if settings.show_swagger_ui else None,
    responses=responses.INTERNAL_SERVER_ERROR,
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
app.include_router(pupils_router)
