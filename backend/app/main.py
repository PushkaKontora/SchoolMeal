from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.children.api.router import router as pupils_router
from app.feedbacks.api.router import router as feedbacks_router
from app.nutrition.api.router import router as nutrition_router
from app.shared.fastapi import responses
from app.shared.fastapi.errors import default_handler
from app.shared.fastapi.settings import FastAPISettings
from app.users.api.router import router as users_router


settings = FastAPISettings()

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
app.include_router(nutrition_router)
