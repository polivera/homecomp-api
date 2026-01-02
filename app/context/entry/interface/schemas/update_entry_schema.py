from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UpdateEntryRequest(BaseModel):
    """Request schema for updating an entry (full update - all fields required)"""

    model_config = ConfigDict(frozen=True)

    account_id: int = Field(..., gt=0, description="Account ID")
    category_id: int = Field(..., gt=0, description="Category ID")
    entry_type: str = Field(..., pattern="^(income|expense)$", description="Entry type (income or expense)")
    entry_date: datetime = Field(..., description="Entry date (timezone-aware)")
    amount: float = Field(..., ge=0, description="Amount (non-negative)")
    description: str = Field(..., max_length=500, description="Entry description")


@dataclass(frozen=True)
class UpdateEntryResponse:
    """Response schema for updating an entry"""

    entry_id: int
    account_id: int
    category_id: int
    entry_type: str
    entry_date: str  # ISO format
    amount: float
    description: str
