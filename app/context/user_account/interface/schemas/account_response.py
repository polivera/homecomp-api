from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AccountResponse:
    account_id: int
    name: str
    currency: str
    balance: Decimal
