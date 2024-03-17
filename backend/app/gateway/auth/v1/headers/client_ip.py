from ipaddress import IPv4Address
from typing import Annotated

from fastapi import Header

from app.identity.domain.rest import Method


ClientIPDep = Annotated[IPv4Address, Header(alias="X-Client-IP", include_in_schema=False)]
RequestURIDep = Annotated[str, Header(alias="X-Original-URI", include_in_schema=False)]
RequestMethodDep = Annotated[Method, Header(alias="X-Original-Method", include_in_schema=False)]
