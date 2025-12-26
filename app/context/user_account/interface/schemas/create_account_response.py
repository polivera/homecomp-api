from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateAccountResponse:
    """Response schema for account creation"""

    account_id: Optional[int]
    account_name: Optional[str]
    account_balance: Optional[float]
