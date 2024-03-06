"""add_status_and_delete_created_at_request_table

Revision ID: ee32c7947efd
Revises: 735ed1dd2b50
Create Date: 2024-03-06 23:09:39.422131

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "ee32c7947efd"
down_revision: Union[str, None] = "735ed1dd2b50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "request", sa.Column("status", sa.Integer(), nullable=False, server_default=sa.text("1")), schema="nutrition"
    )
    op.alter_column("request", "status", server_default=False)

    op.drop_column("request", "created_at", schema="nutrition")


def downgrade() -> None:
    op.add_column(
        "request",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
            server_default=sa.func.now(),
        ),
        schema="nutrition",
    )
    op.drop_column("request", "status", schema="nutrition")
