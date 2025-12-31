"""Unit tests for CreateEntryHandler"""

from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.entry.application.commands import CreateEntryCommand
from app.context.entry.application.dto import CreateEntryErrorCode
from app.context.entry.application.handlers.create_entry_handler import CreateEntryHandler
from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import (
    EntryAccountNotBelongsToUserError,
    EntryCategoryNotBelongsToUserError,
    EntryCategoryNotFoundError,
    EntryMapperError,
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
class TestCreateEntryHandler:
    """Tests for CreateEntryHandler"""

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
        return CreateEntryHandler(mock_service, mock_logger)

    @pytest.mark.asyncio
    async def test_create_entry_success(self, handler, mock_service):
        """Test successful entry creation"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=150.50,
            description="Grocery shopping",
            household_id=3,
        )

        entry_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(entry_date),
            amount=EntryAmount(Decimal("150.50")),
            description=EntryDescription("Grocery shopping"),
            household_id=EntryHouseholdID(3),
        )

        mock_service.create_entry = AsyncMock(return_value=entry_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.entry_id == 100
        assert result.account_id == 10
        assert result.category_id == 5
        assert result.entry_type == "expense"
        assert result.amount == 150.50
        assert result.description == "Grocery shopping"
        mock_service.create_entry.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_entry_without_household_id(self, handler, mock_service):
        """Test creating entry without household_id"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="income",
            entry_date=entry_date,
            amount=1000.00,
            description="Salary",
            household_id=None,
        )

        entry_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.INCOME),
            entry_date=EntryDate(entry_date),
            amount=EntryAmount(Decimal("1000.00")),
            description=EntryDescription("Salary"),
            household_id=None,
        )

        mock_service.create_entry = AsyncMock(return_value=entry_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.entry_id == 100
        # Verify household_id was None in service call
        call_args = mock_service.create_entry.call_args
        assert call_args.kwargs["household_id"] is None

    @pytest.mark.asyncio
    async def test_create_entry_without_entry_id_returns_error(self, handler, mock_service):
        """Test that missing entry_id in result returns error"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
            household_id=None,
        )

        entry_dto = EntryDTO(
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

        mock_service.create_entry = AsyncMock(return_value=entry_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateEntryErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Error creating entry"
        assert result.entry_id is None

    @pytest.mark.asyncio
    async def test_create_entry_account_not_belongs_to_user_error(self, handler, mock_service):
        """Test handling of account not belonging to user exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=999,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
            household_id=None,
        )

        mock_service.create_entry = AsyncMock(
            side_effect=EntryAccountNotBelongsToUserError("Account does not belong to user")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateEntryErrorCode.ACCOUNT_NOT_BELONGS_TO_USER
        assert result.error_message == "Account does not belong to user"
        assert result.entry_id is None

    @pytest.mark.asyncio
    async def test_create_entry_category_not_found_error(self, handler, mock_service):
        """Test handling of category not found exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=999,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
            household_id=None,
        )

        mock_service.create_entry = AsyncMock(side_effect=EntryCategoryNotFoundError("Category not found"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateEntryErrorCode.CATEGORY_NOT_FOUND
        assert result.error_message == "Category not found"
        assert result.entry_id is None

    @pytest.mark.asyncio
    async def test_create_entry_category_not_belongs_to_user_error(self, handler, mock_service):
        """Test handling of category not belonging to user exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=999,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
            household_id=None,
        )

        mock_service.create_entry = AsyncMock(
            side_effect=EntryCategoryNotBelongsToUserError("Category does not belong to user")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateEntryErrorCode.CATEGORY_NOT_BELONGS_TO_USER
        assert result.error_message == "Category does not belong to user"
        assert result.entry_id is None

    @pytest.mark.asyncio
    async def test_create_entry_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
            household_id=None,
        )

        mock_service.create_entry = AsyncMock(side_effect=EntryMapperError("Mapping failed"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateEntryErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping entry data"
        assert result.entry_id is None

    @pytest.mark.asyncio
    async def test_create_entry_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=100.00,
            description="Test",
            household_id=None,
        )

        mock_service.create_entry = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateEntryErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.entry_id is None

    @pytest.mark.asyncio
    async def test_create_entry_converts_primitives_to_value_objects(self, handler, mock_service):
        """Test that handler converts command primitives to value objects"""
        # Arrange
        entry_date = datetime(2024, 12, 31, 10, 0, 0, tzinfo=timezone.utc)
        command = CreateEntryCommand(
            user_id=1,
            account_id=10,
            category_id=5,
            entry_type="expense",
            entry_date=entry_date,
            amount=250.75,
            description="Test Entry",
            household_id=3,
        )

        entry_dto = EntryDTO(
            entry_id=EntryID(100),
            user_id=EntryUserID(1),
            account_id=EntryAccountID(10),
            category_id=EntryCategoryID(5),
            entry_type=EntryType(SharedEntryTypeValues.EXPENSE),
            entry_date=EntryDate(entry_date),
            amount=EntryAmount(Decimal("250.75")),
            description=EntryDescription("Test Entry"),
            household_id=EntryHouseholdID(3),
        )

        mock_service.create_entry = AsyncMock(return_value=entry_dto)

        # Act
        await handler.handle(command)

        # Assert - verify service was called with value objects
        call_args = mock_service.create_entry.call_args
        assert isinstance(call_args.kwargs["user_id"], EntryUserID)
        assert isinstance(call_args.kwargs["account_id"], EntryAccountID)
        assert isinstance(call_args.kwargs["category_id"], EntryCategoryID)
        assert isinstance(call_args.kwargs["entry_type"], EntryType)
        assert isinstance(call_args.kwargs["entry_date"], EntryDate)
        assert isinstance(call_args.kwargs["amount"], EntryAmount)
        assert isinstance(call_args.kwargs["description"], EntryDescription)
        assert isinstance(call_args.kwargs["household_id"], EntryHouseholdID)
