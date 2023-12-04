from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class _Base:
    def dict(self) -> dict[str, Any]:
        excl = ("_sa_adapter", "_sa_instance_state")
        return {k: v for k, v in vars(self).items() if not k.startswith("_") and not any(hasattr(v, a) for a in excl)}


Base = declarative_base(cls=_Base, metadata=MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION))
