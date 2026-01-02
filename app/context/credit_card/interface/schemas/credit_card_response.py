from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CreditCardResponse:
    credit_card_id: int
    user_id: int
    account_id: int
    name: str
    currency: str
    limit: Decimal
    used: Decimal
