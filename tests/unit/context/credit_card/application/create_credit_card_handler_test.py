"""Unit tests for CreateCreditCardHandler"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.credit_card.application.commands import CreateCreditCardCommand
from app.context.credit_card.application.dto import CreateCreditCardErrorCode
from app.context.credit_card.application.handlers.create_credit_card_handler import (
    CreateCreditCardHandler,
)
from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.exceptions import (
    CreditCardMapperError,
    CreditCardNameAlreadyExistError,
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
class TestCreateCreditCardHandler:
    """Tests for CreateCreditCardHandler"""

    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_service):
        """Create handler with mocked service"""
        return CreateCreditCardHandler(mock_service)

    @pytest.mark.asyncio
    async def test_create_credit_card_success(self, handler, mock_service):
        """Test successful credit card creation"""
        # Arrange
        command = CreateCreditCardCommand(
            user_id=1,
            account_id=10,
            name="My Credit Card",
            currency="USD",
            limit=5000.00,
        )

        card_dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Credit Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("5000.00")),
            credit_card_id=CreditCardID(100),
        )

        mock_service.create_credit_card = AsyncMock(return_value=card_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.credit_card_id == 100
        mock_service.create_credit_card.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_credit_card_without_id_returns_error(
        self, handler, mock_service
    ):
        """Test that missing credit_card_id in result returns error"""
        # Arrange
        command = CreateCreditCardCommand(
            user_id=1, account_id=10, name="My Card", currency="USD", limit=1000.00
        )

        card_dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            credit_card_id=None,  # Missing ID
        )

        mock_service.create_credit_card = AsyncMock(return_value=card_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateCreditCardErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Error creating credit card"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_create_credit_card_duplicate_name_error(self, handler, mock_service):
        """Test handling of duplicate name exception"""
        # Arrange
        command = CreateCreditCardCommand(
            user_id=1, account_id=10, name="Duplicate", currency="USD", limit=1000.00
        )

        mock_service.create_credit_card = AsyncMock(
            side_effect=CreditCardNameAlreadyExistError("Duplicate name")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateCreditCardErrorCode.NAME_ALREADY_EXISTS
        assert result.error_message == "Credit card name already exists"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_create_credit_card_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        command = CreateCreditCardCommand(
            user_id=1, account_id=10, name="Test", currency="USD", limit=1000.00
        )

        mock_service.create_credit_card = AsyncMock(
            side_effect=CreditCardMapperError("Mapping failed")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateCreditCardErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping model to dto"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_create_credit_card_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        command = CreateCreditCardCommand(
            user_id=1, account_id=10, name="Test", currency="USD", limit=1000.00
        )

        mock_service.create_credit_card = AsyncMock(
            side_effect=Exception("Database error")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateCreditCardErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_create_credit_card_converts_primitives_to_value_objects(
        self, handler, mock_service
    ):
        """Test that handler converts command primitives to value objects"""
        # Arrange
        command = CreateCreditCardCommand(
            user_id=1,
            account_id=10,
            name="Test Card",
            currency="EUR",
            limit=2500.50,
        )

        card_dto = CreditCardDTO(
            user_id=CreditCardUserID(1),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Test Card"),
            currency=CreditCardCurrency("EUR"),
            limit=CardLimit(Decimal("2500.50")),
            credit_card_id=CreditCardID(100),
        )

        mock_service.create_credit_card = AsyncMock(return_value=card_dto)

        # Act
        await handler.handle(command)

        # Assert - verify service was called with value objects
        call_args = mock_service.create_credit_card.call_args
        assert isinstance(call_args.kwargs["user_id"], CreditCardUserID)
        assert isinstance(call_args.kwargs["account_id"], CreditCardAccountID)
        assert isinstance(call_args.kwargs["name"], CreditCardName)
        assert isinstance(call_args.kwargs["currency"], CreditCardCurrency)
        assert isinstance(call_args.kwargs["limit"], CardLimit)
