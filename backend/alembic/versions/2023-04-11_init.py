"""init

Revision ID: 136439a2e91e
Revises:
Create Date: 2023-04-11 13:23:38.176889

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "136439a2e91e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pupils",
        sa.Column("id", sa.String(length=20), nullable=False),
        sa.Column("last_name", sa.String(length=32), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=False),
        sa.Column("certificate_before_date", sa.DateTime(), nullable=True),
        sa.Column("balance", sa.Float(precision=2, asdecimal=True), nullable=False),
        sa.Column("breakfast", sa.Boolean(), nullable=False),
        sa.Column("lunch", sa.Boolean(), nullable=False),
        sa.Column("dinner", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "schools",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("last_name", sa.String(length=32), nullable=False),
        sa.Column("first_name", sa.String(length=32), nullable=False),
        sa.Column("login", sa.String(length=32), nullable=False),
        sa.Column("role", sa.Enum("PARENT", "TEACHER", "EMPLOYEE", "ORGANIZER", name="role"), nullable=False),
        sa.Column("phone", sa.String(length=12), nullable=True),
        sa.Column("email", sa.String(length=32), nullable=True),
        sa.Column("photo_path", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("login"),
        sa.UniqueConstraint("phone"),
    )
    op.create_table(
        "cancel_meal_periods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("comment", sa.String(length=512), nullable=True),
        sa.ForeignKeyConstraint(["pupil_id"], ["pupils.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "children",
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pupil_id"], ["pupils.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("pupil_id", "parent_id"),
    )
    op.create_table(
        "foods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("photo_path", sa.String(length=128), nullable=False),
        sa.Column("components", sa.String(length=256), nullable=False),
        sa.Column("weight", sa.Float(precision=2), nullable=True),
        sa.Column("kcal", sa.Float(precision=2), nullable=True),
        sa.Column("protein", sa.Float(precision=2), nullable=True),
        sa.Column("fats", sa.Float(precision=2), nullable=True),
        sa.Column("carbs", sa.Float(precision=2), nullable=True),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "issued_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(length=512), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "passwords",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("value", sa.String(length=512), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "school_classes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("letter", sa.String(length=1), nullable=False),
        sa.Column("has_breakfast", sa.Boolean(), nullable=False),
        sa.Column("has_lunch", sa.Boolean(), nullable=False),
        sa.Column("has_dinner", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("school_id", "number", "letter", name="unique_classes_in_school"),
    )
    op.create_table(
        "meals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("breakfast_price", sa.Float(precision=2, asdecimal=True), nullable=False),
        sa.Column("lunch_price", sa.Float(precision=2, asdecimal=True), nullable=False),
        sa.Column("dinner_price", sa.Float(precision=2, asdecimal=True), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["school_classes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("class_id", "date", name="unique_class_meal_per_day"),
    )
    op.create_table(
        "pupils_classes",
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["school_classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pupil_id"], ["pupils.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("class_id", "pupil_id"),
        sa.UniqueConstraint("pupil_id"),
    )
    op.create_table(
        "teachers",
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["school_classes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("class_id", "user_id"),
    )
    op.create_table(
        "meal_requests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("meal_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["meal_id"],
            ["meals.id"],
        ),
        sa.ForeignKeyConstraint(["teacher_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("meal_id"),
    )
    op.create_table(
        "menu",
        sa.Column("meal_id", sa.Integer(), nullable=False),
        sa.Column("food_id", sa.Integer(), nullable=False),
        sa.Column("meal_type", sa.Enum("BREAKFAST", "LUNCH", "DINNER", name="mealtype"), nullable=False),
        sa.ForeignKeyConstraint(["food_id"], ["foods.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["meal_id"], ["meals.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("meal_id", "food_id"),
    )
    op.create_table(
        "declared_pupils",
        sa.Column("request_id", sa.Integer(), nullable=False),
        sa.Column("pupil_id", sa.String(), nullable=False),
        sa.Column("breakfast", sa.Boolean(), nullable=False),
        sa.Column("lunch", sa.Boolean(), nullable=False),
        sa.Column("dinner", sa.Boolean(), nullable=False),
        sa.Column("preferential", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["pupil_id"], ["pupils.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["request_id"], ["meal_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("request_id", "pupil_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("declared_pupils")
    op.drop_table("menu")
    op.drop_table("meal_requests")
    op.drop_table("teachers")
    op.drop_table("pupils_classes")
    op.drop_table("meals")
    op.drop_table("school_classes")
    op.drop_table("passwords")
    op.drop_table("issued_tokens")
    op.drop_table("foods")
    op.drop_table("children")
    op.drop_table("cancel_meal_periods")
    op.drop_table("users")
    op.drop_table("schools")
    op.drop_table("pupils")
    op.execute("DROP TYPE role;")
    op.execute("DROP TYPE mealtype;")
    # ### end Alembic commands ###
