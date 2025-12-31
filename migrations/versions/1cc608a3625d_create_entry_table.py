"""Create Entry Table

Revision ID: 1cc608a3625d
Revises: 93fa43c670c2
Create Date: 2025-12-30 20:43:25.432057

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1cc608a3625d"
down_revision: str | Sequence[str] | None = "93fa43c670c2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create entries table
    op.create_table(
        "entries",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("account_id", sa.Integer, nullable=False),
        sa.Column("category_id", sa.Integer, nullable=False),
        sa.Column(
            "entry_type",
            sa.String(20),
            nullable=False,
        ),
        sa.Column(
            "entry_date",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.DECIMAL(15, 2),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(500),
            nullable=False,
        ),
        sa.Column(
            "household_id",
            sa.Integer,
            nullable=True,  # Optional - for shared household entries
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        # Foreign key constraints
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_entries_user",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["user_accounts.id"],
            name="fk_entries_account",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["household_id"],
            ["households.id"],
            name="fk_entries_household",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name="fk_entries_category",
            ondelete="RESTRICT",
        ),
    )

    # Create indexes for common queries
    op.create_index("ix_entries_user_id", "entries", ["user_id"])
    op.create_index("ix_entries_account_id", "entries", ["account_id"])
    op.create_index("ix_entries_entry_date", "entries", ["entry_date"])
    op.create_index("ix_entries_household_id", "entries", ["household_id"])

    # Composite index for common query pattern: user's entries by date
    op.create_index(
        "ix_entries_user_date",
        "entries",
        ["user_id", "entry_date"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_entries_user_date", table_name="entries")
    op.drop_index("ix_entries_household_id", table_name="entries")
    op.drop_index("ix_entries_entry_date", table_name="entries")
    op.drop_index("ix_entries_account_id", table_name="entries")
    op.drop_index("ix_entries_user_id", table_name="entries")
    op.drop_table("entries")
