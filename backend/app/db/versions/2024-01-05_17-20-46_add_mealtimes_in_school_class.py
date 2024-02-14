"""add_mealtimes_in_school_class

Revision ID: b67be27d0f5d
Revises: cdd45b36be44
Create Date: 2024-01-05 17:20:46.775435

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b67be27d0f5d"
down_revision: Union[str, None] = "cdd45b36be44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "school_class",
        sa.Column("breakfast", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        schema="nutrition",
    )
    op.add_column(
        "school_class",
        sa.Column("dinner", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        schema="nutrition",
    )
    op.add_column(
        "school_class",
        sa.Column("snacks", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        schema="nutrition",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("school_class", "snacks", schema="nutrition")
    op.drop_column("school_class", "dinner", schema="nutrition")
    op.drop_column("school_class", "breakfast", schema="nutrition")
    # ### end Alembic commands ###