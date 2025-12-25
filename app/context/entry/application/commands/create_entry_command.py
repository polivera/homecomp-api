from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class CreateEntryCommand:
    expense_type: str
    expense_date: datetime
    account_id: int
    category_id: int
    household_id: Optional[int]
    amount: float
    description: str
