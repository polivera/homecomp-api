"""create categories table

Revision ID: 93fa43c670c2
Revises: 01770bb99438
Create Date: 2025-12-30 21:05:27.004533

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "93fa43c670c2"
down_revision: str | Sequence[str] | None = "01770bb99438"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "categories",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.String(100), nullable=False, unique=True),  # Globally unique
        sa.Column("color", sa.String(7), nullable=False),  # Hex color code: #RRGGBB
        sa.Column(
            "is_system",
            sa.Boolean,
            nullable=False,
            server_default="false",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # Create indexes for common queries
    op.create_index("ix_categories_deleted_at", "categories", ["deleted_at"])

    # Seed system categories (cannot be modified or deleted)
    op.execute(
        """
        INSERT INTO categories (name, color, is_system)
        VALUES
            ('Uncategorized', '#6B7280', true),
            ('Credit Card Payment', '#EF4444', true)
        """
    )

    # Seed example household categories (can be modified or deleted)
    op.execute(
        """
        INSERT INTO categories (name, color, is_system)
        VALUES
            ('Groceries', '#10B981', false),
            ('Utilities', '#3B82F6', false),
            ('Rent', '#8B5CF6', false),
            ('Transportation', '#F59E0B', false),
            ('Entertainment', '#EC4899', false),
            ('Healthcare', '#06B6D4', false),
            ('Dining Out', '#F97316', false),
            ('Shopping', '#A855F7', false),
            ('Insurance', '#14B8A6', false),
            ('Savings', '#22C55E', false),
            ('Income', '#84CC16', false),
            ('Subscriptions', '#6366F1', false)
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_categories_deleted_at", table_name="categories")
    op.drop_table("categories")
