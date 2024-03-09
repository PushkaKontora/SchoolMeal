"""create_feedbacks_schema

Revision ID: 25153ec6ba38
Revises: d61ef53f01cb
Create Date: 2024-03-09 04:28:13.436099

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "25153ec6ba38"
down_revision: Union[str, None] = "d61ef53f01cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA feedbacks")

    op.create_table(
        "feedback",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("feedback_pkey")),
        schema="feedbacks",
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA feedbacks CASCADE")
