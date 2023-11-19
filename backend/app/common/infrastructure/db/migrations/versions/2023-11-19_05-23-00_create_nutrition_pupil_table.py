"""create_nutrition_pupil_table

Revision ID: e5d8782c9c6d
Revises: dbe87cc52c56
Create Date: 2023-11-19 05:23:00.032908

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e5d8782c9c6d"
down_revision: Union[str, None] = "dbe87cc52c56"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA nutrition")
    op.create_table(
        "pupil",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("meal_plan", sa.JSON(), nullable=False),
        sa.Column("preferential_certificate", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pupil_pkey")),
        schema="nutrition",
    )


def downgrade() -> None:
    op.drop_table("pupil", schema="nutrition")
    op.execute("DROP SCHEMA nutrition")
