"""separate_users_and_feedbacks_tables_by_schemas

Revision ID: 1d273d706f39
Revises: 82afea33cffe
Create Date: 2023-11-11 14:20:37.719143

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "1d273d706f39"
down_revision: Union[str, None] = "82afea33cffe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OLD_AND_NEW_TABLES_MAPPING = [
    ["public.feedback_canteen", "feedbacks.canteen"],
    ["public.user", "users.user"],
    ["public.session", "users.session"],
    ["public.feedback", "feedbacks.feedback"],
]


def upgrade() -> None:
    op.execute("CREATE SCHEMA feedbacks;")
    op.execute("CREATE SCHEMA users;")

    op.create_table(
        "canteen",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("canteen_pkey")),
        schema="feedbacks",
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

    for old_table, new_table in OLD_AND_NEW_TABLES_MAPPING:
        op.execute(f"INSERT INTO {new_table} SELECT * FROM {old_table};")

    op.drop_table("feedback")
    op.drop_table("feedback_canteen")
    op.drop_table("user")
    op.drop_table("session")


def downgrade() -> None:
    op.create_table(
        "feedback_canteen",
        sa.Column("id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="feedback_canteen_pkey"),
    )
    op.create_table(
        "feedback",
        sa.Column("id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("canteen_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("user_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("text", sa.VARCHAR(length=256), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(["canteen_id"], ["feedback_canteen.id"], name="feedback_canteen_id_fkey"),
        sa.PrimaryKeyConstraint("id", name="feedback_pkey"),
    )
    op.create_table(
        "session",
        sa.Column("id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("jti", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("user_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("device_id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("revoked", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="session_pkey"),
    )
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column("login", sa.VARCHAR(length=256), autoincrement=False, nullable=False),
        sa.Column("password", sa.VARCHAR(length=256), autoincrement=False, nullable=False),
        sa.Column("last_name", sa.VARCHAR(length=256), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.VARCHAR(length=256), autoincrement=False, nullable=False),
        sa.Column("role", sa.VARCHAR(length=32), autoincrement=False, nullable=False),
        sa.Column("phone", sa.VARCHAR(length=32), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(length=128), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
        sa.UniqueConstraint("login", name="user_login_key"),
    )

    for old_table, new_table in OLD_AND_NEW_TABLES_MAPPING:
        op.execute(f"INSERT INTO {old_table} SELECT * FROM {new_table};")

    op.drop_table("feedback", schema="feedbacks")
    op.drop_table("canteen", schema="feedbacks")
    op.drop_table("user", schema="users")
    op.drop_table("session", schema="users")

    op.execute("DROP SCHEMA feedbacks;")
    op.execute("DROP SCHEMA users;")
