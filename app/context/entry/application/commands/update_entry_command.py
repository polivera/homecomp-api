from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UpdateEntryCommand:
    """Command for updating an entry"""

    entry_id: int
    user_id: int
    account_id: int
    category_id: int
    entry_type: str
    entry_date: datetime
    amount: float
    description: str
    household_id: int | None = None
