from dataclasses import dataclass
from typing import NewType


SchoolName = NewType("SchoolName", str)


@dataclass
class School:
    name: SchoolName
