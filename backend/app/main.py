from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.common.api.errors import (
    BadRequest,
    LogicError,
    UnprocessableEntity,
    ValidationModelError,
    default_handler,
    logging_http_error_handler,
    logic_error_handler,
    validation_exception_handler,
    validation_model_error_handler,
)
from app.common.api.schemas import HTTPError
from app.common.infrastructure.settings import service
from app.feedbacks.api import router as feedback_router
from app.users.api import router as user_router


app = FastAPI(
    docs_url="/docs" if service.show_swagger_ui else None,
    responses={500: {"model": HTTPError}},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for error_cls in [BadRequest, UnprocessableEntity]:
    app.add_exception_handler(error_cls, logging_http_error_handler)

app.add_exception_handler(BadRequest, logging_http_error_handler)
app.add_exception_handler(LogicError, logic_error_handler)
app.add_exception_handler(ValidationModelError, validation_model_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, default_handler)

app.include_router(user_router)
app.include_router(feedback_router)
