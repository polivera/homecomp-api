"""Unit tests for CreateCreditCardService"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.services.create_credit_card_service import (
    CreateCreditCardService,
)
from app.context.credit_card.domain.value_objects import (
    CardLimit,
    CreditCardAccountID,
    CreditCardCurrency,
    CreditCardID,
    CreditCardName,
    CreditCardUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateCreditCardService:
    """Tests for CreateCreditCardService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create service with mocked repository"""
        return CreateCreditCardService(mock_repository)

    @pytest.mark.asyncio
    async def test_create_credit_card_success(self, service, mock_repository):
        """Test successful credit card creation"""
        # Arrange
        user_id = CreditCardUserID(1)
        account_id = CreditCardAccountID(10)
        name = CreditCardName("My Credit Card")
        currency = CreditCardCurrency("USD")
        limit = CardLimit(Decimal("5000.00"))

        expected_dto = CreditCardDTO(
            user_id=user_id,
            account_id=account_id,
            name=name,
            currency=currency,
            limit=limit,
            credit_card_id=CreditCardID(100),
        )

        mock_repository.save_credit_card = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_credit_card(
            user_id=user_id,
            account_id=account_id,
            name=name,
            currency=currency,
            limit=limit,
        )

        # Assert
        assert result == expected_dto
        mock_repository.save_credit_card.assert_called_once()

        # Verify the DTO passed to save_credit_card has correct values
        call_args = mock_repository.save_credit_card.call_args[0][0]
        assert call_args.user_id == user_id
        assert call_args.account_id == account_id
        assert call_args.name == name
        assert call_args.currency == currency
        assert call_args.limit == limit
        assert call_args.credit_card_id is None  # New card, no ID yet

    @pytest.mark.asyncio
    async def test_create_credit_card_with_different_currencies(
        self, service, mock_repository
    ):
        """Test creating cards with different currency codes"""
        currencies = ["USD", "EUR", "GBP", "JPY"]

        for currency_code in currencies:
            currency = CreditCardCurrency(currency_code)

            expected_dto = CreditCardDTO(
                user_id=CreditCardUserID(1),
                account_id=CreditCardAccountID(10),
                name=CreditCardName("My Card"),
                currency=currency,
                limit=CardLimit(Decimal("1000.00")),
                credit_card_id=CreditCardID(100),
            )

            mock_repository.save_credit_card = AsyncMock(return_value=expected_dto)

            result = await service.create_credit_card(
                user_id=CreditCardUserID(1),
                account_id=CreditCardAccountID(10),
                name=CreditCardName("My Card"),
                currency=currency,
                limit=CardLimit(Decimal("1000.00")),
            )

            assert result.currency.value == currency_code

    @pytest.mark.asyncio
    async def test_create_credit_card_with_high_limit(self, service, mock_repository):
        """Test creating card with high credit limit"""
        # Arrange
        high_limit = CardLimit(Decimal("100000.00"))

        expected_dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Premium Card"),
            currency=CreditCardCurrency("USD"),
            limit=high_limit,
            credit_card_id=CreditCardID(100),
        )

        mock_repository.save_credit_card = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_credit_card(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Premium Card"),
            currency=CreditCardCurrency("USD"),
            limit=high_limit,
        )

        # Assert
        assert result.limit.value == Decimal("100000.00")

    @pytest.mark.asyncio
    async def test_create_credit_card_propagates_repository_exceptions(
        self, service, mock_repository
    ):
        """Test that repository exceptions are propagated"""
        # Arrange
        mock_repository.save_credit_card = AsyncMock(
            side_effect=Exception("Database error")
        )

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.create_credit_card(
                user_id=CreditCardUserID(1),
                account_id=CreditCardAccountID(10),
                name=CreditCardName("My Card"),
                currency=CreditCardCurrency("USD"),
                limit=CardLimit(Decimal("1000.00")),
            )
