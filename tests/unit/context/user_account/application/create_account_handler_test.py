"""Unit tests for CreateAccountHandler"""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.context.user_account.application.handlers.create_account_handler import (
    CreateAccountHandler,
)
from app.context.user_account.application.commands import CreateAccountCommand
from app.context.user_account.application.dto import CreateAccountErrorCode
from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    AccountName,
    UserAccountCurrency,
    UserAccountBalance,
    UserAccountUserID,
)
from app.context.user_account.domain.exceptions import (
    UserAccountNameAlreadyExistError,
    UserAccountMapperError,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateAccountHandler:
    """Tests for CreateAccountHandler"""

    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_service):
        """Create handler with mocked service"""
        return CreateAccountHandler(mock_service)

    @pytest.mark.asyncio
    async def test_create_account_success(self, handler, mock_service):
        """Test successful account creation"""
        # Arrange
        command = CreateAccountCommand(
            user_id=1, name="My Account", currency="USD", balance=100.50
        )

        account_dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            account_id=UserAccountID(10),
        )

        mock_service.create_account = AsyncMock(return_value=account_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.account_id == 10
        assert result.account_name == "My Account"
        assert result.account_balance == 100.50
        mock_service.create_account.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_account_without_id_returns_error(self, handler, mock_service):
        """Test that missing account_id in result returns error"""
        # Arrange
        command = CreateAccountCommand(
            user_id=1, name="My Account", currency="USD", balance=100.00
        )

        account_dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
            account_id=None,  # Missing ID
        )

        mock_service.create_account = AsyncMock(return_value=account_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateAccountErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Error creating account"
        assert result.account_id is None

    @pytest.mark.asyncio
    async def test_create_account_duplicate_name_error(self, handler, mock_service):
        """Test handling of duplicate name exception"""
        # Arrange
        command = CreateAccountCommand(
            user_id=1, name="Duplicate", currency="USD", balance=100.00
        )

        mock_service.create_account = AsyncMock(
            side_effect=UserAccountNameAlreadyExistError("Duplicate name")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateAccountErrorCode.NAME_ALREADY_EXISTS
        assert result.error_message == "Account name already exist"
        assert result.account_id is None

    @pytest.mark.asyncio
    async def test_create_account_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        command = CreateAccountCommand(
            user_id=1, name="Test", currency="USD", balance=100.00
        )

        mock_service.create_account = AsyncMock(
            side_effect=UserAccountMapperError("Mapping failed")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateAccountErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping model to dto"
        assert result.account_id is None

    @pytest.mark.asyncio
    async def test_create_account_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        command = CreateAccountCommand(
            user_id=1, name="Test", currency="USD", balance=100.00
        )

        mock_service.create_account = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateAccountErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.account_id is None

    @pytest.mark.asyncio
    async def test_create_account_converts_primitives_to_value_objects(
        self, handler, mock_service
    ):
        """Test that handler converts command primitives to value objects"""
        # Arrange
        command = CreateAccountCommand(
            user_id=1, name="Test", currency="USD", balance=100.50
        )

        account_dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("Test"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.50")),
            account_id=UserAccountID(10),
        )

        mock_service.create_account = AsyncMock(return_value=account_dto)

        # Act
        await handler.handle(command)

        # Assert - verify service was called with value objects
        call_args = mock_service.create_account.call_args
        assert isinstance(call_args.kwargs["user_id"], UserAccountUserID)
        assert isinstance(call_args.kwargs["name"], AccountName)
        assert isinstance(call_args.kwargs["currency"], UserAccountCurrency)
        assert isinstance(call_args.kwargs["balance"], UserAccountBalance)
