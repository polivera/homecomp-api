"""Create user table

Revision ID: f8333e5b2bac
Revises:
Create Date: 2025-12-21 01:00:30.079504

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f8333e5b2bac"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(100), unique=True, nullable=False),
        sa.Column("password", sa.String(150), nullable=False),
        sa.Column("username", sa.String(100), unique=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
