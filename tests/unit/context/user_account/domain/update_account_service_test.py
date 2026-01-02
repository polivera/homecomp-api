"""Unit tests for UpdateAccountService"""

from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.exceptions import (
    UserAccountNameAlreadyExistError,
    UserAccountNotFoundError,
)
from app.context.user_account.domain.services.update_account_service import (
    UpdateAccountService,
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
class TestUpdateAccountService:
    """Tests for UpdateAccountService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository, mock_logger):
        """Create service with mocked repository"""
        return UpdateAccountService(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_update_account_success(self, service, mock_repository):
        """Test successful account update"""
        # Arrange
        account_id = UserAccountID(10)
        user_id = UserAccountUserID(1)
        name = AccountName("Updated Account")
        currency = UserAccountCurrency("USD")
        balance = UserAccountBalance(Decimal("200.00"))

        existing_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=AccountName("Old Name"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        updated_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
        )

        mock_repository.find_user_account_by_id = AsyncMock(return_value=existing_dto)
        mock_repository.find_user_accounts = AsyncMock(return_value=[])
        mock_repository.update_account = AsyncMock(return_value=updated_dto)

        # Act
        result = await service.update_account(
            account_id=account_id,
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
        )

        # Assert
        assert result == updated_dto
        mock_repository.find_user_account_by_id.assert_called_once_with(user_id=user_id, account_id=account_id)
        mock_repository.update_account.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_account_not_found(self, service, mock_repository):
        """Test updating non-existent account raises error"""
        # Arrange
        account_id = UserAccountID(999)
        user_id = UserAccountUserID(1)

        mock_repository.find_user_account_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(UserAccountNotFoundError, match="Account with ID 999 not found"):
            await service.update_account(
                account_id=account_id,
                user_id=user_id,
                name=AccountName("Test"),
                currency=UserAccountCurrency("USD"),
                balance=UserAccountBalance(Decimal("100.00")),
            )

        mock_repository.find_user_account_by_id.assert_called_once()
        mock_repository.update_account.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_account_name_unchanged(self, service, mock_repository):
        """Test updating account when name doesn't change"""
        # Arrange
        account_id = UserAccountID(10)
        user_id = UserAccountUserID(1)
        name = AccountName("Same Name")  # Same name
        currency = UserAccountCurrency("EUR")
        balance = UserAccountBalance(Decimal("200.00"))

        existing_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=AccountName("Same Name"),  # Same name
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        updated_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
        )

        mock_repository.find_user_account_by_id = AsyncMock(return_value=existing_dto)
        mock_repository.update_account = AsyncMock(return_value=updated_dto)

        # Act
        result = await service.update_account(
            account_id=account_id,
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
        )

        # Assert - should not check for duplicates when name unchanged
        assert result == updated_dto
        mock_repository.find_user_accounts.assert_not_called()
        mock_repository.update_account.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_account_duplicate_name(self, service, mock_repository):
        """Test updating account with duplicate name raises error"""
        # Arrange
        account_id = UserAccountID(10)
        user_id = UserAccountUserID(1)
        new_name = AccountName("Duplicate Name")

        existing_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=AccountName("Old Name"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        # Another account with the same name already exists
        duplicate_dto = UserAccountDTO(
            account_id=UserAccountID(20),  # Different account ID
            user_id=user_id,
            name=new_name,
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("50.00")),
        )

        mock_repository.find_user_account_by_id = AsyncMock(return_value=existing_dto)
        mock_repository.find_user_accounts = AsyncMock(return_value=[duplicate_dto])

        # Act & Assert
        with pytest.raises(
            UserAccountNameAlreadyExistError,
            match="Account with name 'Duplicate Name' already exists",
        ):
            await service.update_account(
                account_id=account_id,
                user_id=user_id,
                name=new_name,
                currency=UserAccountCurrency("USD"),
                balance=UserAccountBalance(Decimal("100.00")),
            )

        mock_repository.update_account.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_account_checks_inactive_accounts_for_duplicates(self, service, mock_repository):
        """Test that duplicate name check includes inactive accounts"""
        # Arrange
        account_id = UserAccountID(10)
        user_id = UserAccountUserID(1)
        new_name = AccountName("New Name")

        existing_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=AccountName("Old Name"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        updated_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=new_name,
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        mock_repository.find_user_account_by_id = AsyncMock(return_value=existing_dto)
        mock_repository.find_user_accounts = AsyncMock(return_value=[])
        mock_repository.update_account = AsyncMock(return_value=updated_dto)

        # Act
        await service.update_account(
            account_id=account_id,
            user_id=user_id,
            name=new_name,
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        # Assert - should check both active and inactive accounts
        mock_repository.find_user_accounts.assert_called_once_with(user_id=user_id, name=new_name, only_active=False)

    @pytest.mark.asyncio
    async def test_update_account_allows_same_account_name(self, service, mock_repository):
        """Test that updating account can keep same name (not duplicate)"""
        # Arrange
        account_id = UserAccountID(10)
        user_id = UserAccountUserID(1)
        new_name = AccountName("Updated Name")

        existing_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=AccountName("Old Name"),
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        # Find returns the same account (not a duplicate, it's the same one)
        same_account_dto = UserAccountDTO(
            account_id=account_id,  # Same account ID
            user_id=user_id,
            name=new_name,
            currency=UserAccountCurrency("USD"),
            balance=UserAccountBalance(Decimal("100.00")),
        )

        updated_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=new_name,
            currency=UserAccountCurrency("EUR"),
            balance=UserAccountBalance(Decimal("200.00")),
        )

        mock_repository.find_user_account_by_id = AsyncMock(return_value=existing_dto)
        mock_repository.find_user_accounts = AsyncMock(return_value=[same_account_dto])
        mock_repository.update_account = AsyncMock(return_value=updated_dto)

        # Act - should succeed because the found account is the same one being updated
        result = await service.update_account(
            account_id=account_id,
            user_id=user_id,
            name=new_name,
            currency=UserAccountCurrency("EUR"),
            balance=UserAccountBalance(Decimal("200.00")),
        )

        # Assert
        assert result == updated_dto
        mock_repository.update_account.assert_called_once()
