from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.infrastructure.models import BaseDBModel


class CategoryModel(BaseDBModel):
    """Minimal category model for validation queries"""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(7), nullable=False)
    household_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("households.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
