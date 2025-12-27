from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CreateCreditCardResponse:
    credit_card_id: int
    name: str
    limit: Decimal
