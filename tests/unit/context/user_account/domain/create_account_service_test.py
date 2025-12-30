"""Unit tests for CreateAccountService"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.services.create_account_service import (
    CreateAccountService,
)
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountID,
    UserAccountUserID,
)
from tests.fixtures.shared.logger import mock_logger


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateAccountService:
    """Tests for CreateAccountService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository, mock_logger):
        """Create service with mocked repository"""
        return CreateAccountService(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_create_account_success(self, service, mock_repository):
        """Test successful account creation"""
        # Arrange
        user_id = UserAccountUserID(1)
        name = AccountName("My Account")
        currency = UserAccountCurrency("USD")
        balance = UserAccountBalance(Decimal("100.00"))

        expected_dto = UserAccountDTO(
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
            account_id=UserAccountID(10),
        )

        mock_repository.save_account = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_account(user_id=user_id, name=name, currency=currency, balance=balance)

        # Assert
        assert result == expected_dto
        mock_repository.save_account.assert_called_once()
        # Verify the DTO passed to save_account has correct values
        call_args = mock_repository.save_account.call_args[0][0]
        assert call_args.user_id == user_id
        assert call_args.name == name
        assert call_args.currency == currency
        assert call_args.balance == balance
        assert call_args.account_id is None  # New account, no ID yet

    @pytest.mark.asyncio
    async def test_create_account_with_zero_balance(self, service, mock_repository):
        """Test creating account with zero balance"""
        # Arrange
        user_id = UserAccountUserID(1)
        name = AccountName("Zero Balance Account")
        currency = UserAccountCurrency("EUR")
        balance = UserAccountBalance(Decimal("0.00"))

        expected_dto = UserAccountDTO(
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
            account_id=UserAccountID(20),
        )

        mock_repository.save_account = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_account(user_id=user_id, name=name, currency=currency, balance=balance)

        # Assert
        assert result.balance.value == Decimal("0.00")
        mock_repository.save_account.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_account_propagates_repository_exceptions(self, service, mock_repository):
        """Test that repository exceptions are propagated"""
        # Arrange
        mock_repository.save_account = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.create_account(
                user_id=UserAccountUserID(1),
                name=AccountName("Test"),
                currency=UserAccountCurrency("USD"),
                balance=UserAccountBalance(Decimal("100.00")),
            )
