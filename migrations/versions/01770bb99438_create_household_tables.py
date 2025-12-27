"""Create household tables

Revision ID: 01770bb99438
Revises: d96343c7a2a6
Create Date: 2025-12-27 15:30:16.811732

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "01770bb99438"
down_revision: Union[str, Sequence[str], None] = "d96343c7a2a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("left_at", sa.DateTime(timezone=True), nullable=True),
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
    )

    # Create index for querying active members by household
    op.create_index(
        "ix_household_members_household_id",
        "household_members",
        ["household_id"],
    )

    # Create index for querying active households by user
    op.create_index(
        "ix_household_members_user_id",
        "household_members",
        ["user_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_household_members_user_id", table_name="household_members")
    op.drop_index("ix_household_members_household_id", table_name="household_members")
    op.drop_table("household_members")
    op.drop_table("households")
