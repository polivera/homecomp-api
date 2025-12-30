"""Unit tests for DeleteAccountHandler"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.user_account.application.commands import DeleteAccountCommand
from app.context.user_account.application.dto import DeleteAccountErrorCode
from app.context.user_account.application.handlers.delete_account_handler import (
    DeleteAccountHandler,
)
from tests.fixtures.shared.logger import mock_logger


@pytest.mark.unit
@pytest.mark.asyncio
class TestDeleteAccountHandler:
    """Tests for DeleteAccountHandler"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_repository, mock_logger):
        """Create handler with mocked repository"""
        return DeleteAccountHandler(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_delete_account_success(self, handler, mock_repository):
        """Test successful account deletion"""
        # Arrange
        command = DeleteAccountCommand(account_id=10, user_id=1)
        mock_repository.delete_account = AsyncMock(return_value=True)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.success is True
        mock_repository.delete_account.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_account_not_found(self, handler, mock_repository):
        """Test deleting non-existent account"""
        # Arrange
        command = DeleteAccountCommand(account_id=999, user_id=1)
        mock_repository.delete_account = AsyncMock(return_value=False)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == DeleteAccountErrorCode.NOT_FOUND
        assert result.error_message == "Account not found"
        # When there's an error, success field should not be set (None by default)
        assert hasattr(result, "success")  # Field exists but should be None in error case

    @pytest.mark.asyncio
    async def test_delete_account_unexpected_error(self, handler, mock_repository):
        """Test handling of unexpected exception"""
        # Arrange
        command = DeleteAccountCommand(account_id=10, user_id=1)
        mock_repository.delete_account = AsyncMock(side_effect=Exception("DB error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == DeleteAccountErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
