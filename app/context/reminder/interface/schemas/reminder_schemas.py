"""Request and response schemas for reminder endpoints"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

# ============================================================================
# Request Schemas (Pydantic for validation)
# ============================================================================


class CreateReminderRequest(BaseModel):
    """Request to create a new reminder"""

    model_config = ConfigDict(frozen=True)

    description: str = Field(..., min_length=1, max_length=500)
    entry_type: str = Field(..., pattern="^(income|expense)$")
    currency: str = Field(..., min_length=3, max_length=3)
    amount: float = Field(..., ge=0, description="Amount (non-negative)")
    frequency: str = Field(..., pattern="^(daily|weekly|biweekly|monthly|quarterly|yearly)$")
    category_id: int
    start_date: datetime
    end_date: datetime | None = None


class UpdateReminderRequest(BaseModel):
    """Request to update a reminder"""

    model_config = ConfigDict(frozen=True)

    description: str | None = Field(None, min_length=1, max_length=500)
    entry_type: str | None = Field(None, pattern="^(income|expense)$")
    currency: str | None = Field(None, min_length=3, max_length=3)
    frequency: str | None = Field(None, pattern="^(daily|weekly|biweekly|monthly|quarterly|yearly)$")
    start_date: datetime | None = None
    end_date: datetime | None = None
    category_id: int | None = None


# ============================================================================
# Response Schemas (Dataclasses for performance)
# ============================================================================


@dataclass(frozen=True)
class ReminderResponse:
    """Response with reminder data"""

    id: int
    description: str
    entry_type: str
    currency: str
    frequency: str
    start_date: datetime
    end_date: datetime | None
    category_id: int | None


@dataclass(frozen=True)
class ReminderListResponse:
    """Response with list of reminders"""

    reminders: list[ReminderResponse]


@dataclass(frozen=True)
class OccurrenceResponse:
    """Response with occurrence data"""

    id: int
    reminder_id: int
    scheduled_date: datetime
    amount: Decimal
    status: str
    entry_id: int | None
    description: str | None
    entry_type: str | None
    currency: str | None
    category_id: int | None


@dataclass(frozen=True)
class OccurrenceListResponse:
    """Response with list of occurrences"""

    occurrences: list[OccurrenceResponse]


@dataclass(frozen=True)
class DeleteReminderResponse:
    """Response for delete reminder operation"""

    message: str


@dataclass(frozen=True)
class PayReminderOccurrenceResponse:
    """Response for pay reminder occurrence operation"""

    paid: bool
    entry_id: int
