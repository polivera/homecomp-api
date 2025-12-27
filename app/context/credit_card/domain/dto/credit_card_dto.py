from dataclasses import dataclass
from typing import Optional

from app.context.credit_card.domain.value_objects import (
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardUserID,
)
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.domain.value_objects.card_used import CardUsed
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)


@dataclass(frozen=True)
class CreditCardDTO:
    """Domain DTO for credit card entity"""

    user_id: CreditCardUserID
    account_id: CreditCardAccountID
    name: CreditCardName
    currency: CreditCardCurrency
    limit: CardLimit
    used: Optional[CardUsed] = None
    credit_card_id: Optional[CreditCardID] = None
