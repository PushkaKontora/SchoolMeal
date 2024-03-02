"""create_feedbacks_schema

Revision ID: ba086e4526f8
Revises: a2b9eadc7fc1
Create Date: 2024-02-16 04:58:16.579945

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ba086e4526f8"
down_revision: Union[str, None] = None
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
