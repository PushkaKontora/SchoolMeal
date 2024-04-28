"""create_triggers

Revision ID: b1ef8ef00896
Revises: 8d4800eab4ea
Create Date: 2024-04-28 12:44:01.654173

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b1ef8ef00896"
down_revision: Union[str, None] = "8d4800eab4ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE FUNCTION nutrition.migrate_users_from_user_management()
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
        CREATE TRIGGER migrate_users_to_nutrition
        AFTER INSERT
        ON user_management.user
        FOR EACH ROW
        EXECUTE FUNCTION nutrition.migrate_users_from_user_management();
    """
    )

    op.execute(
        """
        CREATE FUNCTION nutrition.delete_unregistered_users()
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
    op.execute(
        """
        CREATE TRIGGER delete_users_from_nutrition
        AFTER DELETE
        ON user_management.user
        FOR EACH ROW
        EXECUTE FUNCTION nutrition.delete_unregistered_users();
    """
    )

    op.execute(
        """
        CREATE FUNCTION notification.migrate_users_from_user_management()
            RETURNS trigger AS
        $$
        BEGIN
            INSERT INTO "notification"."user" VALUES (NEW.id, '{}');
            RETURN NEW;
        END;
        $$
        LANGUAGE PLPGSQL;
    """
    )
    op.execute(
        """
        CREATE TRIGGER migrate_users_to_notification
        AFTER INSERT
        ON user_management.user
        FOR EACH ROW
        EXECUTE FUNCTION notification.migrate_users_from_user_management();
    """
    )

    op.execute(
        """
        CREATE FUNCTION notification.delete_unregistered_users()
            RETURNS trigger AS
        $$
        BEGIN
            DELETE FROM "notification"."user" WHERE id = OLD.id;
            RETURN NEW;
        END;
        $$
        LANGUAGE PLPGSQL;
    """
    )
    op.execute(
        """
        CREATE TRIGGER delete_users_from_notification
        AFTER DELETE
        ON user_management.user
        FOR EACH ROW
        EXECUTE FUNCTION notification.delete_unregistered_users();
    """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER migrate_users_to_nutrition ON user_management.user")
    op.execute("DROP FUNCTION nutrition.migrate_users_from_user_management CASCADE")

    op.execute("DROP TRIGGER delete_users_from_nutrition ON user_management.user")
    op.execute("DROP FUNCTION nutrition.delete_unregistered_users CASCADE")

    op.execute("DROP TRIGGER migrate_users_to_notification ON user_management.user")
    op.execute("DROP FUNCTION notification.migrate_users_from_user_management CASCADE")

    op.execute("DROP TRIGGER delete_users_from_notification ON user_management.user")
    op.execute("DROP FUNCTION notification.delete_unregistered_users CASCADE")
