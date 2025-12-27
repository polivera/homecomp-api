from abc import ABC, abstractmethod
from typing import Optional

from app.context.credit_card.domain.dto.credit_card_dto import CreditCardDTO
from app.context.credit_card.domain.value_objects import CreditCardUserID
from app.context.credit_card.domain.value_objects.credit_card_id import CreditCardID
from app.context.credit_card.domain.value_objects.credit_card_name import (
    CreditCardName,
)


class CreditCardRepositoryContract(ABC):
    """Contract for credit card repository operations"""

    @abstractmethod
    async def save_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """
        Create a new credit card

        Args:
            card: The credit card DTO to save

        Returns:
            CreditCardDTO of the created credit card

        Raises:
            CreditCardMapperError if cannot map model to dto
            CreditCardNameAlreadyExistError if card name already exists for user
        """
        pass

    @abstractmethod
    async def find_credit_card(
        self,
        card_id: Optional[CreditCardID] = None,
        user_id: Optional[CreditCardUserID] = None,
        name: Optional[CreditCardName] = None,
        only_active: Optional[bool] = True,
    ) -> Optional[CreditCardDTO]:
        """
        Find a credit card by ID or by user_id and name (admin/unrestricted usage)

        Args:
            card_id: Credit card ID to search for
            user_id: User ID to search for (combined with name)
            name: Credit card name to search for (combined with user_id)
            only_active: Whether to exclude soft-deleted cards (default: True)

        Returns:
            CreditCardDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def find_user_credit_cards(
        self,
        user_id: CreditCardUserID,
        card_id: Optional[CreditCardID] = None,
        name: Optional[CreditCardName] = None,
        only_active: Optional[bool] = True,
    ) -> Optional[list[CreditCardDTO]]:
        """
        Find user credit cards always filtering by user_id (for user-scoped queries)

        Args:
            user_id: User ID to filter cards for
            card_id: Optional card ID to find specific card
            name: Optional card name for partial match search
            only_active: Whether to exclude soft-deleted cards (default: True)

        Returns:
            List of CreditCardDTO, empty list if none found
        """
        pass

    @abstractmethod
    async def find_user_credit_card_by_id(
        self,
        user_id: CreditCardUserID,
        card_id: CreditCardID,
        only_active: Optional[bool] = True,
    ) -> Optional[CreditCardDTO]:
        """
        Find a specific credit card by ID for a user

        Args:
            user_id: User ID who owns the card
            card_id: Credit card ID to find
            only_active: Whether to exclude soft-deleted cards (default: True)

        Returns:
            CreditCardDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_credit_card(self, card: CreditCardDTO) -> CreditCardDTO:
        """
        Update an existing credit card

        Args:
            card: The credit card DTO with updated values

        Returns:
            Updated CreditCardDTO

        Raises:
            ValueError: If card not found or already deleted
        """
        pass

    @abstractmethod
    async def delete_credit_card(
        self, card_id: CreditCardID, user_id: CreditCardUserID
    ) -> bool:
        """
        Soft delete a credit card. Returns True if deleted, False if not found/unauthorized

        Args:
            card_id: Credit card ID to delete
            user_id: User ID (for authorization check)

        Returns:
            True if successfully deleted, False if not found or unauthorized
        """
        pass
