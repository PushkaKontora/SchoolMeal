from typing import Any

from fastapi import status

from app.common.api.schemas import HTTPError


Response = dict[int | str, dict[str, Any]]


BAD_REQUEST: Response = {status.HTTP_400_BAD_REQUEST: {"model": HTTPError}}
UNPROCESSABLE_ENTITY: Response = {status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": HTTPError}}
NOT_FOUND: Response = {status.HTTP_404_NOT_FOUND: {"model": HTTPError}}
FORBIDDEN: Response = {status.HTTP_403_FORBIDDEN: {"model": HTTPError}}
INTERNAL_SERVER_ERROR: Response = {status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPError}}
