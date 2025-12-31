"""Unit tests for CreateEntryService"""

from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotFoundError,
)
from app.context.entry.domain.services.create_entry_service import CreateEntryService
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryHouseholdID,
    EntryID,
    EntryType,
    EntryUserID,
)
from app.shared.domain.value_objects.shared_entry_type import SharedEntryTypeValues


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateEntryService:
    """Tests for CreateEntryService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository, mock_logger):
        """Create service with mocked repository and logger"""
        return CreateEntryService(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_create_entry_success(self, service, mock_repository):
        """Test successful entry creation"""
        # Arrange
        user_id = EntryUserID(1)
        account_id = EntryAccountID(10)
        category_id = EntryCategoryID(5)
        entry_type = EntryType(SharedEntryTypeValues.EXPENSE)
        entry_date = EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc))
        amount = EntryAmount(Decimal("150.50"))
        description = EntryDescription("Grocery shopping")
        household_id = EntryHouseholdID(3)

        expected_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=household_id,
        )

        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.save_entry = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_entry(
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=household_id,
        )

        # Assert
        assert result == expected_dto
        assert result.entry_id == EntryID(100)
        mock_repository.verify_account_belongs_to_user.assert_called_once_with(
            account_id=account_id,
            user_id=user_id,
        )
        mock_repository.verify_category_belongs_to_user.assert_called_once_with(
            category_id=category_id,
            user_id=user_id,
        )
        mock_repository.save_entry.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_entry_without_household_id(self, service, mock_repository):
        """Test creating entry without household_id"""
        # Arrange
        user_id = EntryUserID(1)
        account_id = EntryAccountID(10)
        category_id = EntryCategoryID(5)
        entry_type = EntryType(SharedEntryTypeValues.INCOME)
        entry_date = EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc))
        amount = EntryAmount(Decimal("1000.00"))
        description = EntryDescription("Salary")

        expected_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=None,
        )

        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.save_entry = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_entry(
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=None,
        )

        # Assert
        assert result.household_id is None
        mock_repository.save_entry.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_entry_account_not_belongs_to_user(self, service, mock_repository):
        """Test that creating entry with account not belonging to user raises exception"""
        # Arrange
        user_id = EntryUserID(1)
        account_id = EntryAccountID(999)  # Account doesn't belong to user

        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=False)

        # Act & Assert
        with pytest.raises(
            EntryAccountNotBelongsToUserError,
            match="Account 999 does not belong to user 1",
        ):
            await service.create_entry(
                user_id=user_id,
                account_id=account_id,
                category_id=EntryCategoryID(5),
                entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
                entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)),
                amount=EntryAmount(Decimal("100.00")),
                description=EntryDescription("Test"),
            )

        # Verify category was not checked
        mock_repository.verify_category_belongs_to_user.assert_not_called()
        mock_repository.save_entry.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_entry_category_not_found(self, service, mock_repository):
        """Test that creating entry with invalid category raises exception"""
        # Arrange
        user_id = EntryUserID(1)
        account_id = EntryAccountID(10)
        category_id = EntryCategoryID(999)  # Category doesn't exist or doesn't belong to user

        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=False)

        # Act & Assert
        with pytest.raises(
            EntryCategoryNotFoundError,
            match="Category 999 not found or does not belong to user",
        ):
            await service.create_entry(
                user_id=user_id,
                account_id=account_id,
                category_id=category_id,
                entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
                entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)),
                amount=EntryAmount(Decimal("100.00")),
                description=EntryDescription("Test"),
            )

        # Verify save was not called
        mock_repository.save_entry.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_entry_with_zero_amount(self, service, mock_repository):
        """Test creating entry with zero amount"""
        # Arrange
        user_id = EntryUserID(1)
        account_id = EntryAccountID(10)
        category_id = EntryCategoryID(5)
        entry_type = EntryType(SharedEntryTypeValues.EXPENSE)
        entry_date = EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc))
        amount = EntryAmount(Decimal("0.00"))  # Zero amount
        description = EntryDescription("Refund")

        expected_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=None,
        )

        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.save_entry = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_entry(
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
        )

        # Assert
        assert result.amount.value == Decimal("0.00")

    @pytest.mark.asyncio
    async def test_create_entry_with_income_type(self, service, mock_repository):
        """Test creating entry with INCOME type"""
        # Arrange
        entry_type = EntryType(SharedEntryTypeValues.INCOME)

        expected_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=entry_type,
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)),
            amount=EntryAmount(Decimal("2000.00")),
            description=EntryDescription("Monthly salary"),
            household_id=None,
        )

        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.save_entry = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_entry(
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=entry_type,
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)),
            amount=EntryAmount(Decimal("2000.00")),
            description=EntryDescription("Monthly salary"),
        )

        # Assert
        assert result.entry_type.value == SharedEntryTypeValues.INCOME

    @pytest.mark.asyncio
    async def test_create_entry_propagates_repository_exceptions(self, service, mock_repository):
        """Test that repository exceptions are propagated"""
        # Arrange
        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.save_entry = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.create_entry(
                user_id=EntryUserID(1),
                account_id=EntryAccountID(10),
                category_id=EntryCategoryID(5),
                entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
                entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)),
                amount=EntryAmount(Decimal("100.00")),
                description=EntryDescription("Test"),
            )
