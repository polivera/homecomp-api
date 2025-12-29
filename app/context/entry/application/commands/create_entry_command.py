from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateEntryCommand:
    expense_type: str
    expense_date: datetime
    account_id: int
    category_id: int
    household_id: int | None
    amount: float
    description: str
