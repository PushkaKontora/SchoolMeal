import re
from typing import Annotated

from fastapi import Depends, Header

from app.identity.domain.rest import Method


def _get_request_uri(uri: Annotated[str, Header(alias="X-Original-URI", include_in_schema=False)]) -> str:
    return re.sub(r"^/api", "", uri)


RequestURIDep = Annotated[str, Depends(_get_request_uri)]
RequestMethodDep = Annotated[Method, Header(alias="X-Original-Method", include_in_schema=False)]
