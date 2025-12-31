"""Create credit-cards table

Revision ID: e19a954402db
Revises: d756346442c3
Create Date: 2025-12-25 20:59:00.164701

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e19a954402db"
down_revision: str | Sequence[str] | None = "d756346442c3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "credit_cards",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("account_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100)),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("limit", sa.DECIMAL(15, 2), nullable=False),
        sa.Column("used", sa.DECIMAL(15, 2), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["account_id"], ["user_accounts.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", "name", name="uq_credit_cards_user_id_name"),
    )
    op.create_index("ix_credit_cards_deleted_at", "credit_cards", ["deleted_at"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_credit_cards_deleted_at", table_name="credit_cards")
    op.drop_table("credit_cards")
