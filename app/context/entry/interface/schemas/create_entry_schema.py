from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateEntryRequest(BaseModel):
    """Request schema for creating an entry"""

    model_config = ConfigDict(frozen=True)

    account_id: int = Field(..., gt=0, description="Account ID")
    category_id: int = Field(..., gt=0, description="Category ID")
    entry_type: str = Field(..., pattern="^(income|expense)$", description="Entry type (income or expense)")
    entry_date: datetime = Field(..., description="Entry date (timezone-aware)")
    amount: float = Field(..., ge=0, description="Amount (non-negative)")
    description: str = Field(..., max_length=500, description="Entry description")
    household_id: int | None = Field(None, gt=0, description="Optional household ID")


@dataclass(frozen=True)
class CreateEntryResponse:
    """Response schema for creating an entry"""

    entry_id: int
    account_id: int
    category_id: int
    entry_type: str
    entry_date: str  # ISO format
    amount: float
    description: str
