"""Create Reminders and Reminder Occurrences Tables

Revision ID: a1b2c3d4e5f6
Revises: 1cc608a3625d
Create Date: 2025-12-31 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "1cc608a3625d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create reminders table (stores reminder definitions/templates)
    op.create_table(
        "reminders",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column(
            "entry_type",
            sa.String(20),
            nullable=False,
        ),
        sa.Column(
            "currency",
            sa.String(3),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.DECIMAL(15, 2),
            nullable=False,
        ),
        sa.Column(
            "frequency",
            sa.String(50),
            nullable=False,
        ),
        sa.Column(
            "start_date",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "end_date",
            sa.DateTime(timezone=True),
            nullable=True,  # Optional - for reminders that expire
        ),
        sa.Column(
            "category_id",
            sa.Integer,
            nullable=False,
        ),
        sa.Column(
            "household_id",
            sa.Integer,
            nullable=True,  # Optional - for shared household reminders
        ),
        sa.Column(
            "description",
            sa.String(500),
            nullable=False,
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
            name="fk_reminders_user",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
            name="fk_reminders_category",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["household_id"],
            ["households.id"],
            name="fk_reminders_household",
            ondelete="SET NULL",
        ),
    )

    # Create indexes for reminders
    op.create_index("ix_reminders_user_id", "reminders", ["user_id"])
    op.create_index("ix_reminders_household_id", "reminders", ["household_id"])
    op.create_index("ix_reminders_start_date", "reminders", ["start_date"])
    op.create_index("ix_reminders_frequency", "reminders", ["frequency"])

    # Create reminder_occurrences table (stores generated instances)
    op.create_table(
        "reminder_occurrences",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "reminder_id",
            sa.BigInteger,
            nullable=False,
        ),
        sa.Column(
            "scheduled_date",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "amount",
            sa.DECIMAL(15, 2),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="pending",
        ),
        sa.Column(
            "entry_id",
            sa.BigInteger,
            nullable=True,  # Set when occurrence is converted to an entry
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        # Foreign key constraints
        sa.ForeignKeyConstraint(
            ["reminder_id"],
            ["reminders.id"],
            name="fk_reminder_occurrences_reminder",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["entry_id"],
            ["entries.id"],
            name="fk_reminder_occurrences_entry",
            ondelete="SET NULL",
        ),
    )

    # Create indexes for reminder_occurrences
    op.create_index("ix_reminder_occurrences_reminder_id", "reminder_occurrences", ["reminder_id"])
    op.create_index("ix_reminder_occurrences_scheduled_date", "reminder_occurrences", ["scheduled_date"])
    op.create_index("ix_reminder_occurrences_status", "reminder_occurrences", ["status"])
    # Composite index for finding pending occurrences by date
    op.create_index(
        "ix_reminder_occurrences_status_date",
        "reminder_occurrences",
        ["status", "scheduled_date"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_reminder_occurrences_status_date", table_name="reminder_occurrences")
    op.drop_index("ix_reminder_occurrences_status", table_name="reminder_occurrences")
    op.drop_index("ix_reminder_occurrences_scheduled_date", table_name="reminder_occurrences")
    op.drop_index("ix_reminder_occurrences_reminder_id", table_name="reminder_occurrences")
    op.drop_table("reminder_occurrences")

    op.drop_index("ix_reminders_frequency", table_name="reminders")
    op.drop_index("ix_reminders_start_date", table_name="reminders")
    op.drop_index("ix_reminders_household_id", table_name="reminders")
    op.drop_index("ix_reminders_user_id", table_name="reminders")
    op.drop_table("reminders")
