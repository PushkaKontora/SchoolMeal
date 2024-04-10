"""create_notification_schema

Revision ID: a18a13ac2a6e
Revises: 4888e5ca3370
Create Date: 2024-04-10 20:27:55.789818

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a18a13ac2a6e"
down_revision: Union[str, None] = "4888e5ca3370"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA notification")

    op.create_table(
        "notification",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("recipients", sa.ARRAY(sa.UUID(), dimensions=1), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("subtitle", sa.String(), nullable=False),
        sa.Column("mark", sa.String(), nullable=False),
        sa.Column("body", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("notification_pkey")),
        schema="notification",
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("read_notification_ids", sa.ARRAY(sa.UUID(), dimensions=1), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
        schema="notification",
    )

    op.execute("INSERT INTO notification.user SELECT id, '{}' FROM user_management.user")


def downgrade() -> None:
    op.execute("DROP SCHEMA notification CASCADE")
