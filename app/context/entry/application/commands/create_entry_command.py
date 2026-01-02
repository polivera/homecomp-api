from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateEntryCommand:
    user_id: int
    account_id: int
    category_id: int
    entry_type: str
    entry_date: datetime
    amount: float
    description: str
    household_id: int | None = None
