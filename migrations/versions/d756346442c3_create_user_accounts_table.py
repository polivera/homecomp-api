"""Create user accounts table

Revision ID: d756346442c3
Revises: b8067948709f
Create Date: 2025-12-25 18:44:45.911971

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d756346442c3"
down_revision: Union[str, Sequence[str], None] = "b8067948709f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_accounts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("balance", sa.DECIMAL(15, 2), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", "name", name="uq_user_accounts_user_id_name"),
    )
    op.create_index("ix_user_accounts_deleted_at", "user_accounts", ["deleted_at"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_user_accounts_deleted_at", table_name="user_accounts")
    op.drop_table("user_accounts")
