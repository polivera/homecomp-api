from dataclasses import dataclass


@dataclass(frozen=True)
class FindEntriesByAccountMonthQuery:
    """Query for finding entries by account and month"""

    user_id: int
    account_id: int
    month: int  # 1-12
    year: int  # e.g., 2025
