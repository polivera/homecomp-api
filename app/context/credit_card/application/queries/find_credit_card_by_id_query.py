from dataclasses import dataclass

from app.context.user.domain.value_objects.user_id import UserID
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID


@dataclass(frozen=True)
class FindCreditCardByIdQuery:
    """Query to find a credit card by ID"""

    credit_card_id: CreditCardID
    user_id: UserID
