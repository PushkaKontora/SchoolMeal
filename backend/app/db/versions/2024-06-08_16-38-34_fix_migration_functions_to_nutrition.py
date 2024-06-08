"""fix_migration_functions_to_nutrition

Revision ID: 454675e6b178
Revises: b1ef8ef00896
Create Date: 2024-06-08 16:38:34.089834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '454675e6b178'
down_revision: Union[str, None] = 'b1ef8ef00896'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION nutrition.migrate_users_from_user_management()
            RETURNS trigger AS
        $$
        BEGIN
            CASE NEW.role
                WHEN 0 THEN
                    INSERT INTO "nutrition"."parent" VALUES (NEW.id);
                WHEN 1 THEN
                    INSERT INTO "nutrition"."teacher" VALUES (NEW.id);
                ELSE
                    
            END CASE;
            RETURN NEW;
        END;
        $$
        LANGUAGE PLPGSQL;
    """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION nutrition.delete_unregistered_users()
            RETURNS trigger AS
        $$
        BEGIN
            CASE OLD.role
                WHEN 0 THEN
                    DELETE FROM "nutrition"."parent" WHERE id = OLD.id;
                WHEN 1 THEN
                    DELETE FROM "nutrition"."teacher" WHERE id = OLD.id;
                ELSE
                    
            END CASE;
            RETURN NEW;
        END;
        $$
        LANGUAGE PLPGSQL;
    """
    )


def downgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION nutrition.migrate_users_from_user_management()
            RETURNS trigger AS
        $$
        BEGIN
            CASE NEW.role
                WHEN 0 THEN
                    INSERT INTO "nutrition"."parent" VALUES (NEW.id);
                WHEN 1 THEN
                    INSERT INTO "nutrition"."teacher" VALUES (NEW.id);
            END CASE;
            RETURN NEW;
        END;
        $$
        LANGUAGE PLPGSQL;
    """
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION nutrition.delete_unregistered_users()
            RETURNS trigger AS
        $$
        BEGIN
            CASE OLD.role
                WHEN 0 THEN
                    DELETE FROM "nutrition"."parent" WHERE id = OLD.id;
                WHEN 1 THEN
                    DELETE FROM "nutrition"."teacher" WHERE id = OLD.id;
            END CASE;
            RETURN NEW;
        END;
        $$
        LANGUAGE PLPGSQL;
    """
    )

