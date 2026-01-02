"""Unit tests for CreateHouseholdService"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.context.household.domain.dto import HouseholdDTO
from app.context.household.domain.exceptions import HouseholdNameAlreadyExistError
from app.context.household.domain.services.create_household_service import (
    CreateHouseholdService,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)


@pytest.mark.unit
@pytest.mark.asyncio
class TestCreateHouseholdService:
    """Tests for CreateHouseholdService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return MagicMock()

    @pytest.fixture
    def service(self, mock_repository, mock_logger):
        """Create service with mocked repository and logger"""
        return CreateHouseholdService(mock_repository, mock_logger)

    @pytest.mark.asyncio
    async def test_create_household_success(self, service, mock_repository):
        """Test successful household creation"""
        # Arrange
        name = HouseholdName("Smith Family")
        creator_user_id = HouseholdUserID(1)

        expected_dto = HouseholdDTO(
            household_id=HouseholdID(10),
            owner_user_id=creator_user_id,
            name=name,
        )

        mock_repository.create_household = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_household(name=name, creator_user_id=creator_user_id)

        # Assert
        assert result == expected_dto
        assert result.household_id == HouseholdID(10)
        assert result.owner_user_id == creator_user_id
        assert result.name == name
        mock_repository.create_household.assert_called_once()

        # Verify the DTO passed to create_household
        call_args = mock_repository.create_household.call_args
        passed_dto = call_args.kwargs["household_dto"]
        assert passed_dto.household_id is None  # New household, no ID yet
        assert passed_dto.owner_user_id == creator_user_id
        assert passed_dto.name == name

    @pytest.mark.asyncio
    async def test_create_household_duplicate_name_raises_error(self, service, mock_repository):
        """Test that duplicate household name raises HouseholdNameAlreadyExistError"""
        # Arrange
        name = HouseholdName("Existing Household")
        creator_user_id = HouseholdUserID(1)

        mock_repository.create_household = AsyncMock(
            side_effect=HouseholdNameAlreadyExistError("Household name already exists")
        )

        # Act & Assert
        with pytest.raises(HouseholdNameAlreadyExistError, match="Household name already exists"):
            await service.create_household(name=name, creator_user_id=creator_user_id)

    @pytest.mark.asyncio
    async def test_create_household_propagates_repository_exceptions(self, service, mock_repository):
        """Test that repository exceptions are propagated"""
        # Arrange
        mock_repository.create_household = AsyncMock(side_effect=Exception("Database error"))

        # Act & Assert
        with pytest.raises(Exception, match="Database error"):
            await service.create_household(
                name=HouseholdName("Test"),
                creator_user_id=HouseholdUserID(1),
            )

    @pytest.mark.asyncio
    async def test_create_household_with_long_name(self, service, mock_repository):
        """Test creating household with maximum length name"""
        # Arrange
        long_name = "H" * 100
        name = HouseholdName(long_name)
        creator_user_id = HouseholdUserID(1)

        expected_dto = HouseholdDTO(
            household_id=HouseholdID(20),
            owner_user_id=creator_user_id,
            name=name,
        )

        mock_repository.create_household = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_household(name=name, creator_user_id=creator_user_id)

        # Assert
        assert result.name.value == long_name
        mock_repository.create_household.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_household_with_special_characters(self, service, mock_repository):
        """Test creating household with special characters in name"""
        # Arrange
        name = HouseholdName("Smith's Household #1")
        creator_user_id = HouseholdUserID(1)

        expected_dto = HouseholdDTO(
            household_id=HouseholdID(30),
            owner_user_id=creator_user_id,
            name=name,
        )

        mock_repository.create_household = AsyncMock(return_value=expected_dto)

        # Act
        result = await service.create_household(name=name, creator_user_id=creator_user_id)

        # Assert
        assert result.name == name
        mock_repository.create_household.assert_called_once()
