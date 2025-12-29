"""Unit tests for FindAccountsByUserHandler"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.user_account.application.handlers.find_accounts_by_user_handler import (
    FindAccountsByUserHandler,
)
from app.context.user_account.application.queries import FindAccountsByUserQuery
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
class TestFindAccountsByUserHandler:
    """Tests for FindAccountsByUserHandler"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_repository):
        """Create handler with mocked repository"""
        return FindAccountsByUserHandler(mock_repository)

    @pytest.mark.asyncio
    async def test_find_accounts_by_user_success(self, handler, mock_repository):
        """Test finding all accounts for a user"""
        # Arrange
        query = FindAccountsByUserQuery(user_id=1)

        accounts = [
            UserAccountDTO(
                user_id=UserAccountUserID(1),
                name=AccountName("Account 1"),
                currency=UserAccountCurrency("USD"),
                balance=UserAccountBalance(Decimal("100.00")),
                account_id=UserAccountID(10),
            ),
            UserAccountDTO(
                user_id=UserAccountUserID(1),
                name=AccountName("Account 2"),
                currency=UserAccountCurrency("EUR"),
                balance=UserAccountBalance(Decimal("200.00")),
                account_id=UserAccountID(11),
            ),
        ]

        mock_repository.find_user_accounts = AsyncMock(return_value=accounts)

        # Act
        result = await handler.handle(query)

        # Assert
        assert len(result) == 2
        assert result[0].account_id == 10
        assert result[0].name == "Account 1"
        assert result[1].account_id == 11
        assert result[1].name == "Account 2"

    @pytest.mark.asyncio
    async def test_find_accounts_by_user_empty_list(self, handler, mock_repository):
        """Test finding accounts when user has none"""
        # Arrange
        query = FindAccountsByUserQuery(user_id=1)
        mock_repository.find_user_accounts = AsyncMock(return_value=[])

        # Act
        result = await handler.handle(query)

        # Assert
        assert result == []

    @pytest.mark.asyncio
    async def test_find_accounts_by_user_none_returns_empty_list(
        self, handler, mock_repository
    ):
        """Test that None from repository returns empty list"""
        # Arrange
        query = FindAccountsByUserQuery(user_id=1)
        mock_repository.find_user_accounts = AsyncMock(return_value=None)

        # Act
        result = await handler.handle(query)

        # Assert
        assert result == []
