"""create_nutrition_schema

Revision ID: 735ed1dd2b50
Revises: ba086e4526f8
Create Date: 2024-03-03 03:04:03.763170

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "735ed1dd2b50"
down_revision: Union[str, None] = "ba086e4526f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA nutrition")

    op.create_table(
        "parent",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("children", sa.ARRAY(sa.String(), dimensions=1), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("parent_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "school",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("school_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "teacher",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("teacher_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "school_class",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("teacher_id", sa.Uuid(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("literal", sa.String(length=1), nullable=False),
        sa.Column("mealtimes", sa.ARRAY(sa.Integer(), dimensions=1), nullable=False),
        sa.ForeignKeyConstraint(["teacher_id"], ["nutrition.teacher.id"], name=op.f("school_class_teacher_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("school_class_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "pupil",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=True),
        sa.Column("mealtimes", sa.ARRAY(sa.Integer(), dimensions=1), nullable=False),
        sa.Column("preferential_until", sa.Date(), nullable=True),
        sa.Column("cancellation", sa.ARRAY(sa.Date(), dimensions=2), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["nutrition.school_class.id"], name=op.f("pupil_class_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("pupil_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "request",
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("on_date", sa.Date(), nullable=False),
        sa.Column("mealtimes", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["nutrition.school_class.id"], name=op.f("request_class_id_fkey")),
        sa.PrimaryKeyConstraint("class_id", "on_date", name=op.f("request_pkey")),
        schema="nutrition",
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA nutrition CASCADE")
