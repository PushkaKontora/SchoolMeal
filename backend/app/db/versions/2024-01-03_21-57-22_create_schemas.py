"""create_schemas

Revision ID: 69a74ea1b24c
Revises: ce9faf1f3578
Create Date: 2024-01-03 21:57:22.344218

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "69a74ea1b24c"
down_revision: Union[str, None] = "ce9faf1f3578"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SCHEMAS = ["feedbacks", "nutrition", "users"]


def upgrade() -> None:
    for schema in SCHEMAS:
        op.execute(f"CREATE SCHEMA {schema}")

    op.create_table(
        "canteen",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("canteen_pkey")),
        schema="feedbacks",
    )
    op.create_table(
        "parent",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("parent_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "school",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("school_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "session",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("jti", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("device_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("session_pkey")),
        schema="users",
    )
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("login", sa.String(length=256), nullable=False),
        sa.Column("password", sa.String(length=256), nullable=False),
        sa.Column("last_name", sa.String(length=256), nullable=False),
        sa.Column("first_name", sa.String(length=256), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
        sa.UniqueConstraint("login", name=op.f("user_login_key")),
        schema="users",
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
    op.create_table(
        "school_class",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("school_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("literal", sa.String(length=1), nullable=False),
        sa.ForeignKeyConstraint(["school_id"], ["nutrition.school.id"], name=op.f("school_class_school_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("school_class_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "pupil",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=True),
        sa.Column("has_breakfast", sa.Boolean(), nullable=False),
        sa.Column("has_dinner", sa.Boolean(), nullable=False),
        sa.Column("has_snacks", sa.Boolean(), nullable=False),
        sa.Column("preferential_certificate_ends_at", sa.Date(), nullable=True),
        sa.Column("school_class_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["school_class_id"], ["nutrition.school_class.id"], name=op.f("pupil_school_class_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pupil_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "cancellation_period",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.Column("starts_at", sa.Date(), nullable=False),
        sa.Column("ends_at", sa.Date(), nullable=False),
        sa.Column("reasons", sa.ARRAY(sa.String(), dimensions=1), nullable=False),
        sa.ForeignKeyConstraint(["pupil_id"], ["nutrition.pupil.id"], name=op.f("cancellation_period_pupil_id_fkey")),
        sa.PrimaryKeyConstraint("id", name=op.f("cancellation_period_pkey")),
        schema="nutrition",
    )
    op.create_table(
        "child",
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["nutrition.parent.id"], name=op.f("child_parent_id_fkey")),
        sa.ForeignKeyConstraint(["pupil_id"], ["nutrition.pupil.id"], name=op.f("child_pupil_id_fkey")),
        sa.PrimaryKeyConstraint("parent_id", "pupil_id", name=op.f("child_pkey")),
        schema="nutrition",
    )


def downgrade() -> None:
    for schema in SCHEMAS:
        op.execute(f"DROP SCHEMA {schema} CASCADE")
