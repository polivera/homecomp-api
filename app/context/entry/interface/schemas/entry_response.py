from dataclasses import dataclass


@dataclass(frozen=True)
class EntryResponse:
    """Response schema for entry data"""

    entry_id: int
    user_id: int
    account_id: int
    category_id: int
    entry_type: str
    entry_date: str  # ISO format
    amount: float
    description: str
    household_id: int | None = None
