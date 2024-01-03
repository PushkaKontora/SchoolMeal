"""drop_all_schemas

Revision ID: ce9faf1f3578
Revises: a855171fd99e
Create Date: 2024-01-03 16:11:20.427280

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ce9faf1f3578"
down_revision: Union[str, None] = "a855171fd99e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for schema in ["children", "nutrition", "feedbacks", "users"]:
        op.execute(f"DROP SCHEMA {schema} CASCADE")


def downgrade() -> None:
    raise StopIteration("Необходимо схлопнуть все предыдущие миграции")
