"""Unit tests for UpdateEntryHandler"""

from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.entry.application.commands import UpdateEntryCommand
from app.context.entry.application.dto import UpdateEntryErrorCode
from app.context.entry.application.handlers.update_entry_handler import UpdateEntryHandler
from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotFoundError,
    EntryMapperError,
    EntryNotFoundError,
)
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
class TestUpdateEntryHandler:
    """Tests for UpdateEntryHandler"""

    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        return MagicMock()

    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_service, mock_logger):
        """Create handler with mocked service and logger"""
        return UpdateEntryHandler(mock_service, mock_logger)

    @pytest.mark.asyncio
    async def test_update_entry_success(self, handler, mock_service):
        """Test successful entry update"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=200.00,
            description="Updated description",
        )

        updated_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(entry_date),
            amount=EntryAmount(Decimal("200.00")),
            description=EntryDescription("Updated description"),
            household_id=EntryHouseholdID(3),
        )

        mock_service.update_entry = AsyncMock(return_value=updated_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.entry is not None
        assert result.entry.entry_id == 100
        assert result.entry.account_id == 10
        assert result.entry.category_id == 5
        assert result.entry.entry_type == "expense"
        assert result.entry.amount == 200.00
        assert result.entry.description == "Updated description"
        assert result.entry.household_id == 3
        mock_service.update_entry.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_entry_without_household_id(self, handler, mock_service):
        """Test updating entry without household_id"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=150.00,
            description="Test",
        )

        updated_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(entry_date),
            amount=EntryAmount(Decimal("150.00")),
            description=EntryDescription("Test"),
            household_id=None,
        )

        mock_service.update_entry = AsyncMock(return_value=updated_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.entry.household_id is None

    @pytest.mark.asyncio
    async def test_update_entry_without_entry_id_returns_error(self, handler, mock_service):
        """Test that missing entry_id in result returns error"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
        )

        updated_dto = EntryDTO(
            entry_id=None,  # Missing ID
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(entry_date),
            amount=EntryAmount(Decimal("100.00")),
            description=EntryDescription("Test"),
            household_id=None,
        )

        mock_service.update_entry = AsyncMock(return_value=updated_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateEntryErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Error updating entry"
        assert result.entry is None

    @pytest.mark.asyncio
    async def test_update_entry_not_found_error(self, handler, mock_service):
        """Test handling of entry not found exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=999,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
        )

        mock_service.update_entry = AsyncMock(side_effect=EntryNotFoundError("Entry not found"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateEntryErrorCode.NOT_FOUND
        assert result.error_message == "Entry not found"
        assert result.entry is None

    @pytest.mark.asyncio
    async def test_update_entry_account_not_belongs_to_user_error(self, handler, mock_service):
        """Test handling of account not belonging to user exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=999,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
        )

        mock_service.update_entry = AsyncMock(
            side_effect=EntryAccountNotBelongsToUserError("Account does not belong to user")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateEntryErrorCode.ACCOUNT_NOT_BELONGS_TO_USER
        assert result.error_message == "Account does not belong to user"
        assert result.entry is None

    @pytest.mark.asyncio
    async def test_update_entry_category_not_found_error(self, handler, mock_service):
        """Test handling of category not found exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=10,
            category_id=999,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
        )

        mock_service.update_entry = AsyncMock(side_effect=EntryCategoryNotFoundError("Category not found"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateEntryErrorCode.CATEGORY_NOT_FOUND
        assert result.error_message == "Category not found"
        assert result.entry is None

    @pytest.mark.asyncio
    async def test_update_entry_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
        )

        mock_service.update_entry = AsyncMock(side_effect=EntryMapperError("Mapping failed"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateEntryErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping entry data"
        assert result.entry is None

    @pytest.mark.asyncio
    async def test_update_entry_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
        )

        mock_service.update_entry = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == UpdateEntryErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.entry is None

    @pytest.mark.asyncio
    async def test_update_entry_converts_primitives_to_value_objects(self, handler, mock_service):
        """Test that handler converts command primitives to value objects"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=UTC)
        command = UpdateEntryCommand(
            entry_id=100,
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=250.75,
            description="Updated Entry",
        )

        updated_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(entry_date),
            amount=EntryAmount(Decimal("250.75")),
            description=EntryDescription("Updated Entry"),
            household_id=None,
        )

        mock_service.update_entry = AsyncMock(return_value=updated_dto)

        # Act
        await handler.handle(command)

        # Assert - verify service was called with value objects
        call_args = mock_service.update_entry.call_args
        assert isinstance(call_args.kwargs["entry_id"], EntryID)
        assert isinstance(call_args.kwargs["user_id"], EntryUserID)
        assert isinstance(call_args.kwargs["account_id"], EntryAccountID)
        assert isinstance(call_args.kwargs["category_id"], EntryCategoryID)
        assert isinstance(call_args.kwargs["entry_type"], EntryType)
        assert isinstance(call_args.kwargs["entry_date"], EntryDate)
        assert isinstance(call_args.kwargs["amount"], EntryAmount)
        assert isinstance(call_args.kwargs["description"], EntryDescription)
