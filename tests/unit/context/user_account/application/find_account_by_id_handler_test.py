"""Unit tests for FindAccountByIdHandler"""

import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

from app.context.user_account.application.handlers.find_account_by_id_handler import (
    FindAccountByIdHandler,
)
from app.context.user_account.application.queries import FindAccountByIdQuery
from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    AccountName,
    UserAccountCurrency,
    UserAccountBalance,
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
    def handler(self, mock_repository):
        """Create handler with mocked repository"""
        return FindAccountByIdHandler(mock_repository)

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

        mock_repository.find_user_accounts = AsyncMock(return_value=account_dto)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is not None
        assert result.account_id == 10
        assert result.user_id == 1
        assert result.name == "My Account"
        assert result.currency == "USD"
        assert result.balance == Decimal("100.00")

    @pytest.mark.asyncio
    async def test_find_account_by_id_not_found(self, handler, mock_repository):
        """Test finding non-existent account returns None"""
        # Arrange
        query = FindAccountByIdQuery(account_id=999, user_id=1)
        mock_repository.find_user_accounts = AsyncMock(return_value=None)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_find_account_by_id_calls_repository_with_correct_params(
        self, handler, mock_repository
    ):
        """Test that handler calls repository with correct parameters"""
        # Arrange
        query = FindAccountByIdQuery(account_id=10, user_id=1)
        mock_repository.find_user_accounts = AsyncMock(return_value=None)

        # Act
        await handler.handle(query)

        # Assert
        call_args = mock_repository.find_user_accounts.call_args
        assert isinstance(call_args.kwargs["account_id"], UserAccountID)
        assert call_args.kwargs["account_id"].value == 10
        assert isinstance(call_args.kwargs["user_id"], UserAccountUserID)
        assert call_args.kwargs["user_id"].value == 1
