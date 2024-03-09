"""create_structure_schema

Revision ID: 1e545be04714
Revises: 25153ec6ba38
Create Date: 2024-03-09 04:50:09.459177

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1e545be04714"
down_revision: Union[str, None] = "25153ec6ba38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA structure")

    op.create_table(
        "parent",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("parent_pkey")),
        schema="structure",
    )
    op.create_table(
        "school",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("school_pkey")),
        schema="structure",
    )
    op.create_table(
        "teacher",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("teacher_pkey")),
        schema="structure",
    )
    op.create_table(
        "school_class",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("teacher_id", sa.Uuid(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("literal", sa.String(length=1), nullable=False),
        sa.ForeignKeyConstraint(["teacher_id"], ["structure.teacher.id"], name=op.f("school_class_teacher_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("school_class_pkey")),
        schema="structure",
    )
    op.create_table(
        "pupil",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("class_id", sa.Uuid(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["class_id"], ["structure.school_class.id"], name=op.f("pupil_class_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("pupil_pkey")),
        schema="structure",
    )
    op.create_table(
        "pupil_parent",
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["structure.parent.id"], name=op.f("pupil_parent_parent_id_fkey")),
        sa.ForeignKeyConstraint(["pupil_id"], ["structure.pupil.id"], name=op.f("pupil_parent_pupil_id_fkey")),
        sa.PrimaryKeyConstraint("pupil_id", "parent_id", name=op.f("pupil_parent_pkey")),
        schema="structure",
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA structure CASCADE")
