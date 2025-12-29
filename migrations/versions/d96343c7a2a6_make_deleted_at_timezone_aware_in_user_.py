"""make deleted_at timezone aware in user_accounts

Revision ID: d96343c7a2a6
Revises: e19a954402db
Create Date: 2025-12-27 11:26:08.433758

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d96343c7a2a6"
down_revision: str | Sequence[str] | None = "e19a954402db"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Change deleted_at from TIMESTAMP to TIMESTAMPTZ (timezone-aware)
    op.alter_column(
        "user_accounts",
        "deleted_at",
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert deleted_at from TIMESTAMPTZ back to TIMESTAMP
    op.alter_column(
        "user_accounts",
        "deleted_at",
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=True,
    )
