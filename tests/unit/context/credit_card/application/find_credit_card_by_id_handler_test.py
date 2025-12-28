"""Unit tests for FindCreditCardByIdHandler"""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.context.credit_card.application.handlers.find_credit_card_by_id_handler import (
    FindCreditCardByIdHandler,
)
from app.context.credit_card.application.queries import FindCreditCardByIdQuery
from app.context.credit_card.domain.dto import CreditCardDTO
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
class TestFindCreditCardByIdHandler:
    """Tests for FindCreditCardByIdHandler"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_repository):
        """Create handler with mocked repository"""
        return FindCreditCardByIdHandler(mock_repository)

    @pytest.fixture
    def sample_card_dto(self):
        """Create a sample card DTO"""
        return CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Credit Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("5000.00")),
            used=CardUsed(Decimal("1500.50")),
        )

    @pytest.mark.asyncio
    async def test_find_credit_card_by_id_success(
        self, handler, mock_repository, sample_card_dto
    ):
        """Test successful credit card lookup"""
        # Arrange
        query = FindCreditCardByIdQuery(user_id=100, credit_card_id=1)

        mock_repository.find_user_credit_card_by_id = AsyncMock(
            return_value=sample_card_dto
        )

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result.credit_card_id == 1
        assert result.user_id == 100
        assert result.account_id == 10
        assert result.name == "My Credit Card"
        assert result.currency == "USD"
        assert result.limit == Decimal("5000.00")
        assert result.used == Decimal("1500.50")
        mock_repository.find_user_credit_card_by_id.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_credit_card_by_id_not_found(self, handler, mock_repository):
        """Test credit card not found returns None"""
        # Arrange
        query = FindCreditCardByIdQuery(user_id=100, credit_card_id=999)

        mock_repository.find_user_credit_card_by_id = AsyncMock(return_value=None)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is None
        mock_repository.find_user_credit_card_by_id.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_credit_card_by_id_converts_primitives(
        self, handler, mock_repository, sample_card_dto
    ):
        """Test that handler converts query primitives to value objects"""
        # Arrange
        query = FindCreditCardByIdQuery(user_id=100, credit_card_id=1)

        mock_repository.find_user_credit_card_by_id = AsyncMock(
            return_value=sample_card_dto
        )

        # Act
        await handler.handle(query)

        # Assert - verify repository was called with value objects
        call_args = mock_repository.find_user_credit_card_by_id.call_args
        assert isinstance(call_args.kwargs["user_id"], CreditCardUserID)
        assert call_args.kwargs["user_id"].value == 100
        assert isinstance(call_args.kwargs["card_id"], CreditCardID)
        assert call_args.kwargs["card_id"].value == 1

    @pytest.mark.asyncio
    async def test_find_credit_card_by_id_returns_application_dto(
        self, handler, mock_repository, sample_card_dto
    ):
        """Test that handler returns application layer DTO (not domain DTO)"""
        # Arrange
        query = FindCreditCardByIdQuery(user_id=100, credit_card_id=1)

        mock_repository.find_user_credit_card_by_id = AsyncMock(
            return_value=sample_card_dto
        )

        # Act
        result = await handler.handle(query)

        # Assert - verify result has primitive types (not value objects)
        assert isinstance(result.credit_card_id, int)
        assert isinstance(result.user_id, int)
        assert isinstance(result.account_id, int)
        assert isinstance(result.name, str)
        assert isinstance(result.currency, str)
        assert isinstance(result.limit, Decimal)
        assert isinstance(result.used, Decimal)
