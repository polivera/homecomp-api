from abc import ABC, abstractmethod

from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.value_objects import (
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardUserID,
)
from app.context.credit_card.domain.value_objects.card_limit import CardLimit
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)


class CreateCreditCardServiceContract(ABC):
    """Contract for create credit card service"""

    @abstractmethod
    async def create_credit_card(
        self,
        user_id: CreditCardUserID,
        account_id: CreditCardAccountID,
        name: CreditCardName,
        currency: CreditCardCurrency,
        limit: CardLimit,
    ) -> CreditCardDTO:
        """Create a new credit card"""
        pass
