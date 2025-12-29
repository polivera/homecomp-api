from dataclasses import dataclass

from app.context.credit_card.domain.value_objects import (
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardDeletedAt,
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
    used: CardUsed | None = None
    credit_card_id: CreditCardID | None = None
    deleted_at: CreditCardDeletedAt | None = None

    @property
    def is_deleted(self) -> bool:
        """Check if the credit card is soft deleted"""
        return self.deleted_at is not None
