from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateAccountResult:
    """Result of account creation operation"""

    account_id: Optional[int] = None
    account_name: Optional[str] = None
    account_balance: Optional[float] = None
    error: Optional[str] = None
