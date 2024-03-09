"""create_nutrition_schema

Revision ID: ac36d5b45c8b
Revises: 1e545be04714
Create Date: 2024-03-09 22:16:29.805340

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "ac36d5b45c8b"
down_revision: Union[str, None] = "1e545be04714"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA nutrition")

    op.create_table(
        "school_class",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("mealtimes", sa.ARRAY(sa.Integer(), dimensions=1), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("school_class_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "pupil",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("mealtimes", sa.ARRAY(sa.Integer(), dimensions=1), nullable=False),
        sa.Column("preferential_until", sa.Date(), nullable=True),
        sa.Column("cancelled_periods", sa.ARRAY(sa.Date(), dimensions=2), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["nutrition.school_class.id"], name=op.f("pupil_class_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("pupil_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "request",
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("on_date", sa.Date(), nullable=False),
        sa.Column("mealtimes", sa.ARRAY(sa.Integer(), dimensions=1), nullable=False),
        sa.Column("status", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["nutrition.school_class.id"], name=op.f("request_class_id_fkey")),
        sa.PrimaryKeyConstraint("class_id", "on_date", name=op.f("request_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "declaration",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.Column("mealtimes", sa.ARRAY(sa.Integer(), dimensions=1), nullable=False),
        sa.Column("nutrition", sa.Integer(), nullable=False),
        sa.Column("request_class_id", sa.Uuid(), nullable=False),
        sa.Column("request_on_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["pupil_id"], ["nutrition.pupil.id"], name=op.f("declaration_pupil_id_fkey")),
        sa.ForeignKeyConstraint(
            ["request_class_id", "request_on_date"],
            ["nutrition.request.class_id", "nutrition.request.on_date"],
            name=op.f("declaration_request_class_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("declaration_pkey")),
        schema="nutrition",
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA nutrition CASCADE")
