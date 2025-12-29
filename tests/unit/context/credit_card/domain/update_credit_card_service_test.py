"""Unit tests for UpdateCreditCardService"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.exceptions import (
    CreditCardNameAlreadyExistError,
    CreditCardNotFoundError,
    CreditCardUnauthorizedAccessError,
    CreditCardUsedExceedsLimitError,
)
from app.context.credit_card.domain.services.update_credit_card_service import (
    UpdateCreditCardService,
)
from app.context.credit_card.domain.value_objects import (
    CardLimit,
    CardUsed,
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardID,
    CreditCardName,
    CreditCardUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestUpdateCreditCardService:
    """Tests for UpdateCreditCardService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mocked repository"""
        return UpdateCreditCardService(mock_repository)

    @pytest.fixture
    def existing_card_dto(self):
        """Create an existing card DTO for testing"""
        return CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Old Name"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=CardUsed(Decimal("0.00")),
        )

    @pytest.mark.asyncio
    async def test_update_credit_card_name_success(
        self, service, mock_repository, existing_card_dto
    ):
        """Test successful credit card name update"""
        # Arrange
        new_name = CreditCardName("New Name")

        # First call returns existing card, second call returns None (no duplicate)
        mock_repository.find_credit_card = AsyncMock(
            side_effect=[existing_card_dto, None]
        )

        updated_dto = CreditCardDTO(
            credit_card_id=existing_card_dto.credit_card_id,
            user_id=existing_card_dto.user_id,
            account_id=existing_card_dto.account_id,
            name=new_name,
            currency=existing_card_dto.currency,
            limit=existing_card_dto.limit,
            used=existing_card_dto.used,
        )

        mock_repository.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        result = await service.update_credit_card(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            name=new_name,
        )

        # Assert
        assert result.name.value == "New Name"
        assert mock_repository.find_credit_card.call_count == 2  # Once for card, once for duplicate check
        mock_repository.update_credit_card.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_credit_card_limit_success(
        self, service, mock_repository, existing_card_dto
    ):
        """Test successful credit card limit update"""
        # Arrange
        new_limit = CardLimit(Decimal("5000.00"))

        mock_repository.find_credit_card = AsyncMock(return_value=existing_card_dto)

        updated_dto = CreditCardDTO(
            credit_card_id=existing_card_dto.credit_card_id,
            user_id=existing_card_dto.user_id,
            account_id=existing_card_dto.account_id,
            name=existing_card_dto.name,
            currency=existing_card_dto.currency,
            limit=new_limit,
            used=existing_card_dto.used,
        )

        mock_repository.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        result = await service.update_credit_card(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            limit=new_limit,
        )

        # Assert
        assert result.limit.value == Decimal("5000.00")

    @pytest.mark.asyncio
    async def test_update_credit_card_used_success(
        self, service, mock_repository, existing_card_dto
    ):
        """Test successful credit card used amount update"""
        # Arrange
        new_used = CardUsed(Decimal("500.00"))

        mock_repository.find_credit_card = AsyncMock(return_value=existing_card_dto)

        updated_dto = CreditCardDTO(
            credit_card_id=existing_card_dto.credit_card_id,
            user_id=existing_card_dto.user_id,
            account_id=existing_card_dto.account_id,
            name=existing_card_dto.name,
            currency=existing_card_dto.currency,
            limit=existing_card_dto.limit,
            used=new_used,
        )

        mock_repository.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        result = await service.update_credit_card(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            used=new_used,
        )

        # Assert
        assert result.used.value == Decimal("500.00")

    @pytest.mark.asyncio
    async def test_update_credit_card_not_found_raises_error(
        self, service, mock_repository
    ):
        """Test that updating non-existent card raises CreditCardNotFoundError"""
        # Arrange
        mock_repository.find_credit_card = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(CreditCardNotFoundError, match="Credit card with ID 999 not found"):
            await service.update_credit_card(
                credit_card_id=CreditCardID(999),
                user_id=CreditCardUserID(100),
                name=CreditCardName("New Name"),
            )

    @pytest.mark.asyncio
    async def test_update_credit_card_unauthorized_access_raises_error(
        self, service, mock_repository, existing_card_dto
    ):
        """Test that updating another user's card raises CreditCardUnauthorizedAccessError"""
        # Arrange
        mock_repository.find_credit_card = AsyncMock(return_value=existing_card_dto)

        # Act & Assert
        with pytest.raises(
            CreditCardUnauthorizedAccessError,
            match="User 999 is not authorized to update credit card 1",
        ):
            await service.update_credit_card(
                credit_card_id=CreditCardID(1),
                user_id=CreditCardUserID(999),  # Different user
                name=CreditCardName("New Name"),
            )

    @pytest.mark.asyncio
    async def test_update_credit_card_duplicate_name_raises_error(
        self, service, mock_repository, existing_card_dto
    ):
        """Test that updating to duplicate name raises CreditCardNameAlreadyExistError"""
        # Arrange
        new_name = CreditCardName("Duplicate Name")

        mock_repository.find_credit_card = AsyncMock(
            side_effect=[
                existing_card_dto,  # First call - find existing card
                CreditCardDTO(  # Second call - find duplicate name
                    credit_card_id=CreditCardID(2),
                    user_id=CreditCardUserID(100),
                    account_id=CreditCardAccountID(10),
                    name=new_name,
                    currency=CreditCardCurrency("USD"),
                    limit=CardLimit(Decimal("1000.00")),
                ),
            ]
        )

        # Act & Assert
        with pytest.raises(
            CreditCardNameAlreadyExistError,
            match="Credit card with name 'Duplicate Name' already exists for this user",
        ):
            await service.update_credit_card(
                credit_card_id=CreditCardID(1),
                user_id=CreditCardUserID(100),
                name=new_name,
            )

    @pytest.mark.asyncio
    async def test_update_credit_card_used_exceeds_limit_raises_error(
        self, service, mock_repository, existing_card_dto
    ):
        """Test that setting used > limit raises CreditCardUsedExceedsLimitError"""
        # Arrange
        mock_repository.find_credit_card = AsyncMock(return_value=existing_card_dto)

        # Act & Assert
        with pytest.raises(
            CreditCardUsedExceedsLimitError,
            match="Used amount \\(2000.00\\) cannot exceed limit \\(1000.00\\)",
        ):
            await service.update_credit_card(
                credit_card_id=CreditCardID(1),
                user_id=CreditCardUserID(100),
                used=CardUsed(Decimal("2000.00")),  # Exceeds limit of 1000.00
            )

    @pytest.mark.asyncio
    async def test_update_credit_card_limit_below_used_raises_error(
        self, service, mock_repository
    ):
        """Test that setting limit < used raises CreditCardUsedExceedsLimitError"""
        # Arrange
        card_with_usage = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("5000.00")),
            used=CardUsed(Decimal("3000.00")),  # Currently using 3000
        )

        mock_repository.find_credit_card = AsyncMock(return_value=card_with_usage)

        # Act & Assert
        with pytest.raises(
            CreditCardUsedExceedsLimitError,
            match="Used amount \\(3000.00\\) cannot exceed limit \\(1000.00\\)",
        ):
            await service.update_credit_card(
                credit_card_id=CreditCardID(1),
                user_id=CreditCardUserID(100),
                limit=CardLimit(Decimal("1000.00")),  # New limit below used
            )

    @pytest.mark.asyncio
    async def test_update_credit_card_same_name_no_duplicate_check(
        self, service, mock_repository, existing_card_dto
    ):
        """Test that updating with same name doesn't check for duplicates"""
        # Arrange
        same_name = CreditCardName("Old Name")  # Same as existing

        mock_repository.find_credit_card = AsyncMock(return_value=existing_card_dto)
        mock_repository.update_credit_card = AsyncMock(return_value=existing_card_dto)

        # Act
        await service.update_credit_card(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            name=same_name,
        )

        # Assert - should only call find_credit_card once (not twice for duplicate check)
        assert mock_repository.find_credit_card.call_count == 1
