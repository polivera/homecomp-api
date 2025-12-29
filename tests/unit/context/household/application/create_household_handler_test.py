"""Unit tests for CreateHouseholdHandler"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from app.context.household.application.handlers.create_household_handler import (
    CreateHouseholdHandler,
)
from app.context.household.application.commands import CreateHouseholdCommand
from app.context.household.application.dto import CreateHouseholdErrorCode
from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)
from app.context.household.domain.exceptions import (
    HouseholdMapperError,
    HouseholdNameAlreadyExistError,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateHouseholdHandler:
    """Tests for CreateHouseholdHandler"""

    @pytest.fixture
    def mock_service(self):
        """Create a mock service"""
        return MagicMock()

    @pytest.fixture
    def handler(self, mock_service):
        """Create handler with mocked service"""
        return CreateHouseholdHandler(mock_service)

    @pytest.mark.asyncio
    async def test_create_household_success(self, handler, mock_service):
        """Test successful household creation"""
        # Arrange
        command = CreateHouseholdCommand(user_id=1, name="Smith Family")

        household_dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName("Smith Family"),
        )

        mock_service.create_household = AsyncMock(return_value=household_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.household_id == 10
        assert result.household_name == "Smith Family"
        mock_service.create_household.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_household_without_id_returns_error(self, handler, mock_service):
        """Test that missing household_id in result returns error"""
        # Arrange
        command = CreateHouseholdCommand(user_id=1, name="Smith Family")

        household_dto = HouseholdDTO(
            household_id=None,  # Missing ID
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName("Smith Family"),
        )

        mock_service.create_household = AsyncMock(return_value=household_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateHouseholdErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Error creating household"
        assert result.household_id is None

    @pytest.mark.asyncio
    async def test_create_household_duplicate_name_error(self, handler, mock_service):
        """Test handling of duplicate name exception"""
        # Arrange
        command = CreateHouseholdCommand(user_id=1, name="Duplicate")

        mock_service.create_household = AsyncMock(
            side_effect=HouseholdNameAlreadyExistError("Duplicate name")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateHouseholdErrorCode.NAME_ALREADY_EXISTS
        assert result.error_message == "Household name already exists"
        assert result.household_id is None

    @pytest.mark.asyncio
    async def test_create_household_mapper_error(self, handler, mock_service):
        """Test handling of mapper exception"""
        # Arrange
        command = CreateHouseholdCommand(user_id=1, name="Test")

        mock_service.create_household = AsyncMock(
            side_effect=HouseholdMapperError("Mapping failed")
        )

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateHouseholdErrorCode.MAPPER_ERROR
        assert result.error_message == "Error mapping model to DTO"
        assert result.household_id is None

    @pytest.mark.asyncio
    async def test_create_household_unexpected_error(self, handler, mock_service):
        """Test handling of unexpected exception"""
        # Arrange
        command = CreateHouseholdCommand(user_id=1, name="Test")

        mock_service.create_household = AsyncMock(side_effect=Exception("Database error"))

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code == CreateHouseholdErrorCode.UNEXPECTED_ERROR
        assert result.error_message == "Unexpected error"
        assert result.household_id is None

    @pytest.mark.asyncio
    async def test_create_household_converts_primitives_to_value_objects(
        self, handler, mock_service
    ):
        """Test that handler converts command primitives to value objects"""
        # Arrange
        command = CreateHouseholdCommand(user_id=1, name="Test Household")

        household_dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName("Test Household"),
        )

        mock_service.create_household = AsyncMock(return_value=household_dto)

        # Act
        await handler.handle(command)

        # Assert - verify service was called with value objects
        call_args = mock_service.create_household.call_args
        assert isinstance(call_args.kwargs["name"], HouseholdName)
        assert isinstance(call_args.kwargs["creator_user_id"], HouseholdUserID)
        assert call_args.kwargs["name"].value == "Test Household"
        assert call_args.kwargs["creator_user_id"].value == 1

    @pytest.mark.asyncio
    async def test_create_household_with_long_name(self, handler, mock_service):
        """Test creating household with maximum length name"""
        # Arrange
        long_name = "H" * 100
        command = CreateHouseholdCommand(user_id=1, name=long_name)

        household_dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=HouseholdUserID(1),
            name=HouseholdName(long_name),
        )

        mock_service.create_household = AsyncMock(return_value=household_dto)

        # Act
        result = await handler.handle(command)

        # Assert
        assert result.error_code is None
        assert result.household_name == long_name
