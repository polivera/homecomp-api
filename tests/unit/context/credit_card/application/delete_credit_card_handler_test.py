"""Unit tests for DeleteCreditCardHandler"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.credit_card.application.commands import DeleteCreditCardCommand
from app.context.credit_card.application.dto import DeleteCreditCardErrorCode
from app.context.credit_card.application.handlers.delete_credit_card_handler import (
    DeleteCreditCardHandler,
)
from app.context.credit_card.domain.exceptions import CreditCardNotFoundError


@pytest.mark.unit
@pytest.mark.asyncio
class TestDeleteCreditCardHandler:
    """Tests for DeleteCreditCardHandler"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_repository):
        """Create handler with mocked repository"""
        return DeleteCreditCardHandler(mock_repository)

    @pytest.mark.asyncio
    async def test_delete_credit_card_success(self, handler, mock_repository):
        """Test successful credit card deletion"""
        # Arrange
        command = DeleteCreditCardCommand(credit_card_id=1, user_id=100)

        mock_repository.delete_credit_card = AsyncMock(return_value=True)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.success is True
        mock_repository.delete_credit_card.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_credit_card_not_found_returns_error(self, handler, mock_repository):
        """Test that deleting non-existent card returns error"""
        # Arrange
        command = DeleteCreditCardCommand(credit_card_id=999, user_id=100)

        mock_repository.delete_credit_card = AsyncMock(return_value=False)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == DeleteCreditCardErrorCode.NOT_FOUND
        assert result.error_message == "Credit card not found"
        assert result.success is False

    @pytest.mark.asyncio
    async def test_delete_credit_card_not_found_exception(self, handler, mock_repository):
        """Test handling of not found exception"""
        # Arrange
        command = DeleteCreditCardCommand(credit_card_id=999, user_id=100)

        mock_repository.delete_credit_card = AsyncMock(side_effect=CreditCardNotFoundError("Card not found"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == DeleteCreditCardErrorCode.NOT_FOUND
        assert result.error_message == "Credit card not found"
        assert result.success is False

    @pytest.mark.asyncio
    async def test_delete_credit_card_unexpected_error(self, handler, mock_repository):
        """Test handling of unexpected exception"""
        # Arrange
        command = DeleteCreditCardCommand(credit_card_id=1, user_id=100)

        mock_repository.delete_credit_card = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == DeleteCreditCardErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.success is False
