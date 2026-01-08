"""Saga State ORM Model - Saga Orchestration Pattern."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.models.base_model import BaseDBModel


class SagaStateModel(BaseDBModel):
    """
    Saga State model for tracking saga execution state.

    Each saga represents a multi-step distributed transaction.
    This model tracks the current state of each saga execution.

    Status transitions:
    - initiated → entry_created → completed (happy path)
    - initiated → compensating → failed (error path)
    - Any → failed (unrecoverable error)
    """

    __tablename__ = "saga_state"

    saga_id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID as string
    saga_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "PayReminderSaga"

    # Current status of saga execution
    status: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # initiated, entry_created, completed, failed, compensating

    # Saga payload (stores context data for the saga)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
