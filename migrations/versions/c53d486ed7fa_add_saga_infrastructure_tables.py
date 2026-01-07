"""add saga infrastructure tables

Revision ID: c53d486ed7fa
Revises: a1b2c3d4e5f6
Create Date: 2026-01-05 22:21:48.701136

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c53d486ed7fa"
down_revision: str | Sequence[str] | None = "a1b2c3d4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create message_queue table (transactional outbox)
    op.create_table(
        "message_queue",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("event_data", sa.JSON(), nullable=False),
        sa.Column("saga_id", sa.String(36), nullable=False),  # UUID as string
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
    )

    # Create indexes for message_queue
    op.create_index("idx_message_queue_status", "message_queue", ["status"])
    op.create_index("idx_message_queue_saga_id", "message_queue", ["saga_id"])

    # Create saga_state table
    op.create_table(
        "saga_state",
        sa.Column("saga_id", sa.String(36), primary_key=True),  # UUID as string
        sa.Column("saga_type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Create index for saga_state
    op.create_index("idx_saga_state_status", "saga_state", ["status"])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes first
    op.drop_index("idx_saga_state_status", table_name="saga_state")
    op.drop_index("idx_message_queue_saga_id", table_name="message_queue")
    op.drop_index("idx_message_queue_status", table_name="message_queue")

    # Drop tables
    op.drop_table("saga_state")
    op.drop_table("message_queue")
