from abc import ABC, abstractmethod
from typing import Optional

from app.context.user.domain.value_objects.user_id import UserID
from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)


class CreditCardRepositoryContract(ABC):
    """Contract for credit card repository operations"""

    @abstractmethod
    async def save_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """Create a new credit card"""
        pass

    @abstractmethod
    async def find_credit_card(
        self,
        card_id: Optional[CreditCardID] = None,
        user_id: Optional[UserID] = None,
        name: Optional[CreditCardName] = None,
    ) -> Optional[CreditCardDTO]:
        """Find a credit card by ID or by user_id and name"""
        pass

    @abstractmethod
    async def find_credit_cards_by_user(self, user_id: UserID) -> list[CreditCardDTO]:
        """Find all non-deleted credit cards for a user"""
        pass

    @abstractmethod
    async def update_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """Update an existing credit card"""
        pass

    @abstractmethod
    async def delete_credit_card(
        self, card_id: CreditCardID, user_id: UserID
    ) -> bool:
        """Soft delete a credit card. Returns True if deleted, False if not found/unauthorized"""
        pass
