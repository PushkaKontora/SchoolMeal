"""create_identity_schema

Revision ID: 905ce42cbf83
Revises: ac36d5b45c8b
Create Date: 2024-03-16 17:36:41.064120

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "905ce42cbf83"
down_revision: Union[str, None] = "ac36d5b45c8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA identity")

    op.create_table(
        "user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("login", sa.String(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("role", sa.Integer(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
        schema="identity",
    )
    op.create_table(
        "session",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("fingerprint", sa.String(), nullable=False),
        sa.Column("ip", sa.String(), nullable=False),
        sa.Column("expires_in", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["identity.user.id"], name=op.f("session_user_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("session_pkey")),
        schema="identity",
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA identity CASCADE")
