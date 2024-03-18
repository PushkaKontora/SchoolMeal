"""rename_identity_schema_to_user_management

Revision ID: 4888e5ca3370
Revises: 7e8c5d117aeb
Create Date: 2024-03-18 15:23:32.952555

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4888e5ca3370"
down_revision: Union[str, None] = "7e8c5d117aeb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER SCHEMA identity RENAME TO user_management")


def downgrade() -> None:
    op.execute("ALTER SCHEMA user_management RENAME TO identity")
