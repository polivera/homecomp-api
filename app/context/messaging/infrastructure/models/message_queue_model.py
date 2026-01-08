"""Message Queue ORM Model - Transactional Outbox Pattern."""

from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.models.base_model import BaseDBModel


class MessageQueueModel(BaseDBModel):
    """
    Message Queue model for the transactional outbox pattern.

    Stores events that need to be processed by background workers.
    Events are written to this table in the same transaction as the business operation,
    ensuring atomic delivery (no dual writes problem).

    Background workers poll this table and dispatch events to handlers.
    """

    __tablename__ = "message_queue"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    event_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    saga_id: Mapped[str] = mapped_column(String(36), nullable=False)  # UUID as string

    # Event processing status
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending, processing, completed, failed

    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )

    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True, default=None)
