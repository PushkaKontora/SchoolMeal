from ipaddress import IPv4Address
from typing import Annotated

from fastapi import Header


ClientIPDep = Annotated[IPv4Address, Header(alias="X-Client-IP", include_in_schema=False)]
