from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.account.api import router as accounts_router
from app.common.api.errors import (
    LogicError,
    ValidationModelError,
    default_handler,
    logic_error_handler,
    validation_exception_handler,
    validation_model_error_handler,
)
from app.common.api.schemas import HTTPError
from app.common.infrastructure.settings import service


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

app.add_exception_handler(LogicError, logic_error_handler)
app.add_exception_handler(ValidationModelError, validation_model_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, default_handler)

app.include_router(accounts_router, prefix="/accounts")
