from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.models import BaseDBModel


class EntryModel(BaseDBModel):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    account_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user_accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    entry_type: Mapped[str] = mapped_column(String(20), nullable=False)
    entry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    household_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("households.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
