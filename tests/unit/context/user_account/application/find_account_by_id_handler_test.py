"""Unit tests for FindAccountByIdHandler"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.user_account.application.dto.find_single_account_result import (
    FindSingleAccountErrorCode,
)
from app.context.user_account.application.handlers.find_account_by_id_handler import (
    FindAccountByIdHandler,
)
from app.context.user_account.application.queries import FindAccountByIdQuery
from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountID,
    UserAccountUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestFindAccountByIdHandler:
    """Tests for FindAccountByIdHandler"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_repository, mock_logger):
        """Create handler with mocked repository"""
        return FindAccountByIdHandler(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_find_account_by_id_success(self, handler, mock_repository):
        """Test finding account by ID successfully"""
        # Arrange
        query = FindAccountByIdQuery(account_id=10, user_id=1)

        account_dto = UserAccountDTO(
            user_id=UserAccountUserID(1),
            name=AccountName("My Account"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
            account_id=UserAccountID(10),
        )

        # Handler expects a list from the repository
        mock_repository.find_user_accounts = AsyncMock(return_value=[account_dto])

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result.error_code is None
        assert result.error_message is None
        assert result.account is not None
        assert result.account.account_id == 10
        assert result.account.user_id == 1
        assert result.account.name == "My Account"
        assert result.account.currency == "USD"
        assert result.account.balance == Decimal("100.00")

    @pytest.mark.asyncio
    async def test_find_account_by_id_not_found(self, handler, mock_repository):
        """Test finding non-existent account returns error result"""
        # Arrange
        query = FindAccountByIdQuery(account_id=999, user_id=1)
        # Repository returns None when account not found
        mock_repository.find_user_accounts = AsyncMock(return_value=None)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result.error_code == FindSingleAccountErrorCode.NOT_FOUND
        assert result.error_message == "No account found"
        assert result.account is None

    @pytest.mark.asyncio
    async def test_find_account_by_id_calls_repository_with_correct_params(self, handler, mock_repository):
        """Test that handler calls repository with correct parameters"""
        # Arrange
        query = FindAccountByIdQuery(account_id=10, user_id=1)
        # Return empty list to test repository call without affecting test focus
        mock_repository.find_user_accounts = AsyncMock(return_value=[])

        # Act
        await handler.handle(query)

        # Assert
        call_args = mock_repository.find_user_accounts.call_args
        assert isinstance(call_args.kwargs["account_id"], UserAccountID)
        assert call_args.kwargs["account_id"].value == 10
        assert isinstance(call_args.kwargs["user_id"], UserAccountUserID)
        assert call_args.kwargs["user_id"].value == 1

    @pytest.mark.asyncio
    async def test_find_account_by_id_empty_list_returns_not_found(self, handler, mock_repository):
        """Test finding account when repository returns empty list"""
        # Arrange
        query = FindAccountByIdQuery(account_id=999, user_id=1)
        # Repository returns empty list when account not found
        mock_repository.find_user_accounts = AsyncMock(return_value=[])

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result.error_code == FindSingleAccountErrorCode.NOT_FOUND
        assert result.error_message == "No account found"
        assert result.account is None
