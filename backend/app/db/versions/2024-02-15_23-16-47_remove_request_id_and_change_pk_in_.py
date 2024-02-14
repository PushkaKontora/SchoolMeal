"""remove_request_id_and_change_pk_in_request

Revision ID: 946e631e1fd1
Revises: bf71cb5318e6
Create Date: 2024-02-15 23:16:47.803042

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "946e631e1fd1"
down_revision: Union[str, None] = "bf71cb5318e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("request", "id", schema="nutrition")
    op.create_primary_key("request_pkey", "request", ["class_id", "on_date"], schema="nutrition")


def downgrade() -> None:
    op.add_column("request", sa.Column("id", sa.UUID(), autoincrement=False, nullable=False), schema="nutrition")
    op.drop_constraint("request_pkey", "request", schema="nutrition")
    op.create_primary_key("request_pkey", "request", ["id"], schema="nutrition")
