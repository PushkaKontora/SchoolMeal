"""drop_all_schemas

Revision ID: 9369a85e9610
Revises: ed3db230074d
Create Date: 2024-02-15 02:27:18.418612

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9369a85e9610"
down_revision: Union[str, None] = "ed3db230074d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for schema in ["nutrition", "feedbacks", "users"]:
        op.execute(f"DROP SCHEMA {schema} CASCADE")


def downgrade() -> None:
    raise StopIteration("Необходимо схлопнуть все предыдущие миграции")
