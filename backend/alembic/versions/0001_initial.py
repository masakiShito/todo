"""initial

Revision ID: 0001
Revises: 
Create Date: 2024-01-01
"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    task_status = sa.Enum("backlog", "in_progress", "review", "done", name="taskstatus")
    task_priority = sa.Enum("P0", "P1", "P2", "P3", name="taskpriority")
    task_status.create(op.get_bind(), checkfirst=True)
    task_priority.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("color", sa.String(length=30), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_categories_id", "categories", ["id"], unique=False)
    op.create_index("ix_categories_user_id", "categories", ["user_id"], unique=False)

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", task_status, nullable=False),
        sa.Column("priority", task_priority, nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("estimate_hours", sa.Integer(), nullable=True),
        sa.Column("tags", pg.JSONB(), nullable=True),
        sa.Column("parent_task_id", sa.Integer(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"]),
        sa.ForeignKeyConstraint(["parent_task_id"], ["tasks.id"]),
    )
    op.create_index("ix_tasks_id", "tasks", ["id"], unique=False)
    op.create_index("ix_tasks_user_id", "tasks", ["user_id"], unique=False)
    op.create_index("idx_tasks_status", "tasks", ["status"], unique=False)
    op.create_index("idx_tasks_due_date", "tasks", ["due_date"], unique=False)
    op.create_index("idx_tasks_category", "tasks", ["category_id"], unique=False)
    op.create_index("idx_tasks_parent", "tasks", ["parent_task_id"], unique=False)


def downgrade():
    op.drop_index("idx_tasks_parent", table_name="tasks")
    op.drop_index("idx_tasks_category", table_name="tasks")
    op.drop_index("idx_tasks_due_date", table_name="tasks")
    op.drop_index("idx_tasks_status", table_name="tasks")
    op.drop_index("ix_tasks_user_id", table_name="tasks")
    op.drop_index("ix_tasks_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_index("ix_categories_user_id", table_name="categories")
    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")
    task_status = sa.Enum("backlog", "in_progress", "review", "done", name="taskstatus")
    task_priority = sa.Enum("P0", "P1", "P2", "P3", name="taskpriority")
    task_status.drop(op.get_bind(), checkfirst=True)
    task_priority.drop(op.get_bind(), checkfirst=True)
