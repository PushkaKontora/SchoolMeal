from typing import Any

from fastapi import status

from app.common.api.schemas import HTTPError


BAD_REQUEST: dict[int | str, dict[str, Any]] = {status.HTTP_400_BAD_REQUEST: {"model": HTTPError}}
UNPROCESSABLE_ENTITY: dict[int | str, dict[str, Any]] = {status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": HTTPError}}
NOT_FOUND: dict[int | str, dict[str, Any]] = {status.HTTP_404_NOT_FOUND: {"model": HTTPError}}
INTERNAL_SERVER_ERROR: dict[int | str, dict[str, Any]] = {status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPError}}
