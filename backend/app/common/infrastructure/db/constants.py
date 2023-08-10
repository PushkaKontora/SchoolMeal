from enum import Enum


CASCADE = "CASCADE"
SET_NULL = "SET NULL"


class LazyMode(str, Enum):
    NO_LOAD = "noload"
