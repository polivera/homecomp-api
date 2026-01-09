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
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("color", sa.String(7), nullable=False),  # Hex color code: #RRGGBB
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
        # Foreign key constraints
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_categories_user",
            ondelete="CASCADE",
        ),
        # Unique constraint: user can't have duplicate category names
        sa.UniqueConstraint(
            "user_id",
            "name",
            name="uq_categories_user_name",
        ),
    )

    # Create indexes for common queries
    op.create_index("ix_categories_user_id", "categories", ["user_id"])
    op.create_index("ix_categories_deleted_at", "categories", ["deleted_at"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_categories_deleted_at", table_name="categories")
    op.drop_index("ix_categories_user_id", table_name="categories")
    op.drop_table("categories")
