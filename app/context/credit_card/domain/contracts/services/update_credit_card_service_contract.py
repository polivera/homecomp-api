from abc import ABC, abstractmethod
from typing import Optional

from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.value_objects import (
    CreditCardCurrency,
    CreditCardUserID,
)
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.domain.value_objects.card_used import CardUsed
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)


class UpdateCreditCardServiceContract(ABC):
    """Contract for update credit card service"""

    @abstractmethod
    async def update_credit_card(
        self,
        credit_card_id: CreditCardID,
        user_id: CreditCardUserID,
        name: Optional[CreditCardName] = None,
        limit: Optional[CardLimit] = None,
        used: Optional[CardUsed] = None,
        currency: Optional[CreditCardCurrency] = None,
    ) -> CreditCardDTO:
        """Update an existing credit card"""
        pass
