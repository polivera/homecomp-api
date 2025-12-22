"""Create session table

Revision ID: b8067948709f
Revises: f8333e5b2bac
Create Date: 2025-12-22 11:43:45.188730

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b8067948709f"
down_revision: Union[str, Sequence[str], None] = "f8333e5b2bac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sessions",
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("token", sa.String(100), nullable=True, unique=True, index=True),
        sa.Column("failed_attempts", sa.Integer, default=0),
        sa.Column("blocked_until", sa.DateTime, nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("sessions")
