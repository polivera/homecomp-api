from datetime import UTC, datetime

from sqlalchemy import DECIMAL, BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.models import BaseDBModel


class ReminderOccurrenceModel(BaseDBModel):
    __tablename__ = "reminder_occurrences"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    reminder_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("reminders.id", ondelete="CASCADE"),
        nullable=False,
    )
    scheduled_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount: Mapped[int] = mapped_column(DECIMAL(15, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    entry_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        default=None,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
