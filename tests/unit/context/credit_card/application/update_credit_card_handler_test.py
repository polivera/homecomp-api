"""Unit tests for UpdateCreditCardHandler"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.credit_card.application.commands import UpdateCreditCardCommand
from app.context.credit_card.application.dto import UpdateCreditCardErrorCode
from app.context.credit_card.application.handlers.update_credit_card_handler import (
    UpdateCreditCardHandler,
)
from app.context.credit_card.domain.dto import CreditCardDTO
from app.context.credit_card.domain.exceptions import (
    CreditCardMapperError,
    CreditCardNameAlreadyExistError,
    CreditCardNotFoundError,
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
class TestUpdateCreditCardHandler:
    """Tests for UpdateCreditCardHandler"""

    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_service):
        """Create handler with mocked service"""
        return UpdateCreditCardHandler(mock_service)

    @pytest.mark.asyncio
    async def test_update_credit_card_success(self, handler, mock_service):
        """Test successful credit card update"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name="Updated Name",
            currency=None,
            limit=None,
            used=None,
        )

        updated_dto = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Updated Name"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=CardUsed(Decimal("0.00")),
        )

        mock_service.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.credit_card_id == 1
        assert result.credit_card_name == "Updated Name"
        mock_service.update_credit_card.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_credit_card_limit_success(self, handler, mock_service):
        """Test successful credit card limit update"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name=None,
            currency=None,
            limit=5000.00,
            used=None,
        )

        updated_dto = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("5000.00")),
            used=CardUsed(Decimal("0.00")),
        )

        mock_service.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.credit_card_id == 1

    @pytest.mark.asyncio
    async def test_update_credit_card_used_success(self, handler, mock_service):
        """Test successful credit card used amount update"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name=None,
            currency=None,
            limit=None,
            used=500.00,
        )

        updated_dto = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("My Card"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=CardUsed(Decimal("500.00")),
        )

        mock_service.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.credit_card_id == 1

    @pytest.mark.asyncio
    async def test_update_credit_card_not_found_error(self, handler, mock_service):
        """Test handling of not found exception"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=999,
            user_id=100,
            name="New Name",
            currency=None,
            limit=None,
            used=None,
        )

        mock_service.update_credit_card = AsyncMock(side_effect=CreditCardNotFoundError("Card not found"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateCreditCardErrorCode.NOT_FOUND
        assert result.error_message == "Credit card not found"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_update_credit_card_duplicate_name_error(self, handler, mock_service):
        """Test handling of duplicate name exception"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name="Duplicate",
            currency=None,
            limit=None,
            used=None,
        )

        mock_service.update_credit_card = AsyncMock(side_effect=CreditCardNameAlreadyExistError("Duplicate name"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateCreditCardErrorCode.NAME_ALREADY_EXISTS
        assert result.error_message == "Credit card name already exists"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_update_credit_card_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name="Test",
            currency=None,
            limit=None,
            used=None,
        )

        mock_service.update_credit_card = AsyncMock(side_effect=CreditCardMapperError("Mapping failed"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateCreditCardErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping model to dto"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_update_credit_card_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name="Test",
            currency=None,
            limit=None,
            used=None,
        )

        mock_service.update_credit_card = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateCreditCardErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.credit_card_id is None

    @pytest.mark.asyncio
    async def test_update_credit_card_converts_primitives_to_value_objects(self, handler, mock_service):
        """Test that handler converts command primitives to value objects"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name="Updated",
            currency="EUR",
            limit=2500.50,
            used=500.25,
        )

        updated_dto = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Updated"),
            currency=CreditCardCurrency("EUR"),
            limit=CardLimit(Decimal("2500.50")),
            used=CardUsed(Decimal("500.25")),
        )

        mock_service.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        await handler.handle(command)

        # Assert - verify service was called with value objects
        call_args = mock_service.update_credit_card.call_args
        assert isinstance(call_args.kwargs["credit_card_id"], CreditCardID)
        assert isinstance(call_args.kwargs["user_id"], CreditCardUserID)
        assert isinstance(call_args.kwargs["name"], CreditCardName)
        assert isinstance(call_args.kwargs["currency"], CreditCardCurrency)
        assert isinstance(call_args.kwargs["limit"], CardLimit)
        assert isinstance(call_args.kwargs["used"], CardUsed)

    @pytest.mark.asyncio
    async def test_update_credit_card_with_none_values_converts_correctly(self, handler, mock_service):
        """Test that handler handles None values correctly"""
        # Arrange
        command = UpdateCreditCardCommand(
            credit_card_id=1,
            user_id=100,
            name="Updated",
            currency=None,  # None values should result in None, not value objects
            limit=None,
            used=None,
        )

        updated_dto = CreditCardDTO(
            credit_card_id=CreditCardID(1),
            user_id=CreditCardUserID(100),
            account_id=CreditCardAccountID(10),
            name=CreditCardName("Updated"),
            currency=CreditCardCurrency("USD"),
            limit=CardLimit(Decimal("1000.00")),
            used=CardUsed(Decimal("0.00")),
        )

        mock_service.update_credit_card = AsyncMock(return_value=updated_dto)

        # Act
        await handler.handle(command)

        # Assert - verify None values are passed as None
        call_args = mock_service.update_credit_card.call_args
        assert call_args.kwargs["currency"] is None
        assert call_args.kwargs["limit"] is None
        assert call_args.kwargs["used"] is None
