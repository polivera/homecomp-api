"""Unit tests for UpdateAccountHandler"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.user_account.application.commands import UpdateAccountCommand
from app.context.user_account.application.dto import UpdateAccountErrorCode
from app.context.user_account.application.handlers.update_account_handler import (
    UpdateAccountHandler,
)
from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.exceptions import (
    UserAccountMapperError,
    UserAccountNameAlreadyExistError,
    UserAccountNotFoundError,
)
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountID,
    UserAccountUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestUpdateAccountHandler:
    """Tests for UpdateAccountHandler"""

    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_service):
        """Create handler with mocked service"""
        return UpdateAccountHandler(mock_service)

    @pytest.mark.asyncio
    async def test_update_account_success(self, handler, mock_service):
        """Test successful account update"""
        # Arrange
        command = UpdateAccountCommand(account_id=10, user_id=1, name="Updated", currency="EUR", balance=200.00)

        updated_dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("Updated"),
            currency=UserAccountCurrency("EUR"),
            balance=UserAccountBalance(Decimal("200.00")),
            account_id=UserAccountID(10),
        )

        mock_service.update_account = AsyncMock(return_value=updated_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.account_id == 10
        assert result.account_name == "Updated"
        assert result.account_balance == 200.00

    @pytest.mark.asyncio
    async def test_update_account_not_found(self, handler, mock_service):
        """Test handling of account not found exception"""
        # Arrange
        command = UpdateAccountCommand(account_id=999, user_id=1, name="Test", currency="USD", balance=100.00)

        mock_service.update_account = AsyncMock(side_effect=UserAccountNotFoundError("Not found"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateAccountErrorCode.NOT_FOUND
        assert result.error_message == "Account not found"

    @pytest.mark.asyncio
    async def test_update_account_duplicate_name(self, handler, mock_service):
        """Test handling of duplicate name exception"""
        # Arrange
        command = UpdateAccountCommand(account_id=10, user_id=1, name="Duplicate", currency="USD", balance=100.00)

        mock_service.update_account = AsyncMock(side_effect=UserAccountNameAlreadyExistError("Duplicate"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateAccountErrorCode.NAME_ALREADY_EXISTS
        assert result.error_message == "Account name already exist"

    @pytest.mark.asyncio
    async def test_update_account_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        command = UpdateAccountCommand(account_id=10, user_id=1, name="Test", currency="USD", balance=100.00)

        mock_service.update_account = AsyncMock(side_effect=UserAccountMapperError("Mapping failed"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateAccountErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping model to dto"

    @pytest.mark.asyncio
    async def test_update_account_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        command = UpdateAccountCommand(account_id=10, user_id=1, name="Test", currency="USD", balance=100.00)

        mock_service.update_account = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateAccountErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
