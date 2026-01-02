"""Unit tests for UpdateEntryService"""

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotFoundError,
    EntryNotFoundError,
)
from app.context.entry.domain.services.update_entry_service import UpdateEntryService
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
class TestUpdateEntryService:
    """Tests for UpdateEntryService"""

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
        return UpdateEntryService(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_update_entry_success(self, service, mock_repository):
        """Test successful entry update"""
        # Arrange
        entry_id = EntryID(100)
        user_id = EntryUserID(1)
        account_id = EntryAccountID(10)
        category_id = EntryCategoryID(5)
        entry_type = EntryType(SharedEntryTypeValues.EXPENSE)
        entry_date = EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC))
        amount = EntryAmount(Decimal("200.00"))
        description = EntryDescription("Updated description")
        household_id = EntryHouseholdID(3)

        # Existing entry with household_id
        existing_entry = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(4),  # Different category
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 30, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("100.00")),
            description=EntryDescription("Old description"),
            household_id=household_id,
        )

        updated_dto = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
            household_id=household_id,  # Preserved from existing
        )

        mock_repository.find_entry_by_id = AsyncMock(return_value=existing_entry)
        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.update_entry = AsyncMock(return_value=updated_dto)

        # Act
        result = await service.update_entry(
            entry_id=entry_id,
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            entry_type=entry_type,
            entry_date=entry_date,
            amount=amount,
            description=description,
        )

        # Assert
        assert result == updated_dto
        assert result.household_id == household_id  # Preserved
        mock_repository.find_entry_by_id.assert_called_once_with(
            entry_id=entry_id,
            user_id=user_id,
        )
        mock_repository.verify_account_belongs_to_user.assert_called_once()
        mock_repository.verify_category_belongs_to_user.assert_called_once()
        mock_repository.update_entry.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_entry_not_found(self, service, mock_repository):
        """Test updating non-existent entry raises exception"""
        # Arrange
        entry_id = EntryID(999)
        user_id = EntryUserID(1)

        mock_repository.find_entry_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(
            EntryNotFoundError,
            match="Entry 999 not found or does not belong to user",
        ):
            await service.update_entry(
                entry_id=entry_id,
                user_id=user_id,
                account_id=EntryAccountID(10),
                category_id=EntryCategoryID(5),
                entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
                entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
                amount=EntryAmount(Decimal("100.00")),
                description=EntryDescription("Test"),
            )

        # Verify subsequent checks were not performed
        mock_repository.verify_account_belongs_to_user.assert_not_called()
        mock_repository.verify_category_belongs_to_user.assert_not_called()
        mock_repository.update_entry.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_entry_account_not_belongs_to_user(self, service, mock_repository):
        """Test updating entry with account not belonging to user raises exception"""
        # Arrange
        entry_id = EntryID(100)
        user_id = EntryUserID(1)
        account_id = EntryAccountID(999)  # Account doesn't belong to user

        existing_entry = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 30, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("100.00")),
            description=EntryDescription("Old"),
            household_id=None,
        )

        mock_repository.find_entry_by_id = AsyncMock(return_value=existing_entry)
        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=False)

        # Act & Assert
        with pytest.raises(
            EntryAccountNotBelongsToUserError,
            match="Account 999 does not belong to user 1",
        ):
            await service.update_entry(
                entry_id=entry_id,
                user_id=user_id,
                account_id=account_id,
                category_id=EntryCategoryID(5),
                entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
                entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
                amount=EntryAmount(Decimal("100.00")),
                description=EntryDescription("Test"),
            )

        # Verify category and update were not called
        mock_repository.verify_category_belongs_to_user.assert_not_called()
        mock_repository.update_entry.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_entry_category_not_found(self, service, mock_repository):
        """Test updating entry with invalid category raises exception"""
        # Arrange
        entry_id = EntryID(100)
        user_id = EntryUserID(1)
        category_id = EntryCategoryID(999)  # Category doesn't exist

        existing_entry = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 30, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("100.00")),
            description=EntryDescription("Old"),
            household_id=None,
        )

        mock_repository.find_entry_by_id = AsyncMock(return_value=existing_entry)
        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=False)

        # Act & Assert
        with pytest.raises(
            EntryCategoryNotFoundError,
            match="Category 999 not found or does not belong to user",
        ):
            await service.update_entry(
                entry_id=entry_id,
                user_id=user_id,
                account_id=EntryAccountID(10),
                category_id=category_id,
                entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
                entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
                amount=EntryAmount(Decimal("100.00")),
                description=EntryDescription("Test"),
            )

        # Verify update was not called
        mock_repository.update_entry.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_entry_preserves_household_id(self, service, mock_repository):
        """Test that update preserves household_id from existing entry"""
        # Arrange
        entry_id = EntryID(100)
        user_id = EntryUserID(1)
        household_id = EntryHouseholdID(5)

        existing_entry = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 30, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("100.00")),
            description=EntryDescription("Old"),
            household_id=household_id,  # Has household_id
        )

        updated_dto = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("200.00")),
            description=EntryDescription("Updated"),
            household_id=household_id,  # Preserved
        )

        mock_repository.find_entry_by_id = AsyncMock(return_value=existing_entry)
        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.update_entry = AsyncMock(return_value=updated_dto)

        # Act
        result = await service.update_entry(
            entry_id=entry_id,
            user_id=user_id,
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("200.00")),
            description=EntryDescription("Updated"),
            household_id=EntryHouseholdID(5),
        )

        # Assert
        assert result.household_id == household_id
        # Verify the DTO passed to update_entry had household_id preserved
        call_args = mock_repository.update_entry.call_args[0][0]
        assert call_args.household_id == household_id

    @pytest.mark.asyncio
    async def test_update_entry_propagates_repository_exceptions(self, service, mock_repository):
        """Test that repository exceptions are propagated"""
        # Arrange
        entry_id = EntryID(100)
        user_id = EntryUserID(1)

        existing_entry = EntryDTO(
            entry_id=entry_id,
            user_id=user_id,
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(datetime(2024, 12, 30, 10, 0, 0, tzinfo=UTC)),
            amount=EntryAmount(Decimal("100.00")),
            description=EntryDescription("Old"),
            household_id=None,
        )

        mock_repository.find_entry_by_id = AsyncMock(return_value=existing_entry)
        mock_repository.verify_account_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.verify_category_belongs_to_user = AsyncMock(return_value=True)
        mock_repository.update_entry = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.update_entry(
                entry_id=entry_id,
                user_id=user_id,
                account_id=EntryAccountID(10),
                category_id=EntryCategoryID(5),
                entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
                entry_date=EntryDate(datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)),
                amount=EntryAmount(Decimal("100.00")),
                description=EntryDescription("Test"),
            )
