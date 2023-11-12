"""create_feedback_and_canteen_tables

Revision ID: c32d5dd24f1b
Revises: c20f08889b01
Create Date: 2023-11-12 17:07:19.150608

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c32d5dd24f1b"
down_revision: Union[str, None] = "c20f08889b01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA feedbacks;")

    op.create_table(
        "canteen",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("canteen_pkey")),
        schema="feedbacks",
    )
    op.create_table(
        "feedback",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("canteen_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("text", sa.String(length=256), nullable=False),
        sa.ForeignKeyConstraint(["canteen_id"], ["feedbacks.canteen.id"], name=op.f("feedback_canteen_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("feedback_pkey")),
        schema="feedbacks",
    )


def downgrade() -> None:
    op.drop_table("feedback", schema="feedbacks")
    op.drop_table("canteen", schema="feedbacks")
    op.execute("DROP SCHEME feedbacks;")
