"""Create household tables

Revision ID: 01770bb99438
Revises: d96343c7a2a6
Create Date: 2025-12-27 15:30:16.811732

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "01770bb99438"
down_revision: str | Sequence[str] | None = "d96343c7a2a6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create households table
    op.create_table(
        "households",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("owner_user_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        # Foreign key to users table
        sa.ForeignKeyConstraint(
            ["owner_user_id"],
            ["users.id"],
            name="fk_households_owner_user",
            ondelete="RESTRICT",
        ),
        # Composite unique constraint: owner can't have duplicate household names
        sa.UniqueConstraint(
            "owner_user_id",
            "name",
            name="uq_households_owner_name",
        ),
    )

    # Create household_members join table
    op.create_table(
        "household_members",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("household_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column(
            "role",
            sa.String(20),
            nullable=False,
            server_default="participant",
        ),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            nullable=True,  # NULL for invited members, set when they accept
        ),
        sa.Column("invited_by_user_id", sa.Integer, nullable=True),
        sa.Column(
            "invited_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(
            ["household_id"],
            ["households.id"],
            name="fk_household_members_household",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_household_members_user",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["invited_by_user_id"],
            ["users.id"],
            name="fk_household_members_inviter",
            ondelete="RESTRICT",
        ),
        # Composite unique constraint - user can only have one record per household
        sa.UniqueConstraint("household_id", "user_id", name="uq_household_user"),
    )

    # Partial index: Get user's active households
    # Used for: "What households do I have access to?"
    op.create_index(
        "ix_household_members_user_active",
        "household_members",
        ["user_id"],
        postgresql_where=sa.text("joined_at IS NOT NULL"),
    )

    # Partial index: Check if user has access to specific household
    # Used for: "Does user X have access to household Y?"
    op.create_index(
        "ix_household_members_access_check",
        "household_members",
        ["household_id", "user_id"],
        postgresql_where=sa.text("joined_at IS NOT NULL"),
    )

    # Partial index: Get user's pending invites
    # Used for: "What households has user been invited to?"
    op.create_index(
        "ix_household_members_pending_invites",
        "household_members",
        ["user_id"],
        postgresql_where=sa.text("joined_at IS NULL"),
    )

    # Partial index: Get household's pending invites (for owner to see)
    # Used for: "Who has owner invited to this household?"
    op.create_index(
        "ix_household_members_household_pending",
        "household_members",
        ["household_id"],
        postgresql_where=sa.text("joined_at IS NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_household_members_household_pending", table_name="household_members")
    op.drop_index("ix_household_members_pending_invites", table_name="household_members")
    op.drop_index("ix_household_members_access_check", table_name="household_members")
    op.drop_index("ix_household_members_user_active", table_name="household_members")
    op.drop_table("household_members")
    op.drop_table("households")
